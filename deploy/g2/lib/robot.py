"""机器人后端：内存模拟，以及 GDK 阻塞关节控制。"""

from __future__ import annotations

from typing import Protocol

import numpy as np

from .joints import ACTION_DIM, ARM_DOF, ARM_NAMES, JointLayout, make_layout


class Robot(Protocol):
    def read_radians(self) -> np.ndarray:
        """长度 16，前 14 个为手臂弧度，后 2 个为夹爪行程。"""

    def read_status(self) -> dict:
        """急停与错误码。全 0 / False 表示可以动。"""

    def move_arms(self, positions: np.ndarray, velocity: float) -> None:
        """阻塞直到双臂到达目标，或底层抛错。"""

    def move_grippers(self, positions: np.ndarray) -> None:
        """阻塞直到双夹爪到达目标。positions 为 [左, 右] 物理行程。"""

    def close(self) -> None:
        ...


def _clean_status() -> dict:
    return {
        "left_arm_error": 0,
        "right_arm_error": 0,
        "left_end_error": 0,
        "right_end_error": 0,
        "left_arm_estop": False,
        "right_arm_estop": False,
    }


class MockRobot:
    """不连真机。姿态存在内存里，move_* 立即到达。"""

    def __init__(self, layout: JointLayout | None = None, q: np.ndarray | None = None):
        self.layout = layout or make_layout()
        if q is None:
            q = (self.layout.limits[:, 0] + self.layout.limits[:, 1]) / 2.0
        self.q = np.asarray(q, dtype=np.float64).copy()
        if self.q.shape != (ACTION_DIM,):
            raise ValueError(f"初始姿态长度应为 {ACTION_DIM}")
        self.status = _clean_status()
        self.arm_commands: list[np.ndarray] = []
        self.arm_velocities: list[np.ndarray] = []
        self.gripper_commands: list[np.ndarray] = []

    def read_radians(self) -> np.ndarray:
        return self.q.copy()

    def read_status(self) -> dict:
        return dict(self.status)

    def move_arms(self, positions: np.ndarray, velocity) -> None:
        target = np.asarray(positions, dtype=np.float64)
        speed = _arm_velocities(velocity)
        if target.shape != (ARM_DOF,):
            raise ValueError(f"手臂指令长度应为 {ARM_DOF}")
        self.arm_commands.append(target.copy())
        self.arm_velocities.append(speed)
        self.q[:ARM_DOF] = target

    def move_grippers(self, positions: np.ndarray) -> None:
        target = np.asarray(positions, dtype=np.float64)
        if target.shape != (2,):
            raise ValueError("夹爪指令长度应为 2")
        self.gripper_commands.append(target.copy())
        self.q[ARM_DOF:] = target

    def close(self) -> None:
        return None


def _arm_velocities(velocity) -> np.ndarray:
    speed = np.asarray(velocity, dtype=np.float64)
    if speed.ndim == 0:
        speed = np.full(ARM_DOF, float(speed))
    if speed.shape != (ARM_DOF,):
        raise ValueError(f"手臂速度长度应为 {ARM_DOF}")
    if np.any(speed <= 0) or not np.all(np.isfinite(speed)):
        raise ValueError("手臂速度必须是正数")
    return speed


def _joint_position(state: dict) -> float:
    if "motor_position" in state and state["motor_position"] is not None:
        return float(state["motor_position"])
    return float(state["position"])


def _gripper_position(side: dict) -> float:
    states = side.get("end_states") or []
    if not states:
        raise RuntimeError(f"末端状态为空: names={side.get('names')}")
    return float(states[0]["position"])


class GdkRobot:
    """通过 GDK 阻塞接口控制 G2 双臂和双夹爪。

    手臂使用 move_arm_joint(..., control_group=2)，该接口规划到目标后才返回。
    不使用 joint_servo_control：伺服通道要 100Hz 连发，低延时模式没有碰撞保护。
    """

    def __init__(self, layout: JointLayout | None = None, init_sleep_s: float = 1.0):
        from .gdk_session import ensure_gdk

        self.layout = layout or make_layout()
        self._gdk = ensure_gdk()
        self._robot = self._gdk.Robot()
        if init_sleep_s > 0:
            import time

            time.sleep(init_sleep_s)

    def read_radians(self) -> np.ndarray:
        joint_states = self._robot.get_joint_states()
        by_name = {state["name"]: state for state in joint_states["states"]}
        missing = [name for name in ARM_NAMES if name not in by_name]
        if missing:
            raise RuntimeError(f"关节状态缺少 {missing}")
        arms = np.array([_joint_position(by_name[name]) for name in ARM_NAMES], dtype=np.float64)
        end = self._robot.get_end_state()
        left = _gripper_position(end["left_end_state"])
        right = _gripper_position(end["right_end_state"])
        return np.concatenate([arms, [left, right]])

    def read_status(self) -> dict:
        status = self._robot.get_whole_body_status()
        return {
            "left_arm_error": int(status.get("left_arm_error", 0) or 0),
            "right_arm_error": int(status.get("right_arm_error", 0) or 0),
            "left_end_error": int(status.get("left_end_error", 0) or 0),
            "right_end_error": int(status.get("right_end_error", 0) or 0),
            "left_arm_estop": bool(status.get("left_arm_estop", False)),
            "right_arm_estop": bool(status.get("right_arm_estop", False)),
        }

    def move_arms(self, positions: np.ndarray, velocity) -> None:
        target = [float(v) for v in np.asarray(positions, dtype=np.float64)]
        if len(target) != ARM_DOF:
            raise ValueError(f"手臂指令长度应为 {ARM_DOF}")
        velocities = [float(v) for v in _arm_velocities(velocity)]
        # control_group=2：同时规划左右臂，调用返回时运动已结束。
        # velocities 是各关节走向目标的速度，单位 rad/s，取正值。
        self._robot.move_arm_joint(target, velocities, 2)

    def move_grippers(self, positions: np.ndarray) -> None:
        left_pos, right_pos = (float(v) for v in np.asarray(positions, dtype=np.float64))
        joint_states = self._gdk.JointStates()
        joint_states.group = "dual_tool"
        joint_states.target_type = self.layout.gripper_type
        left = self._gdk.JointState()
        right = self._gdk.JointState()
        left.position = left_pos
        right.position = right_pos
        joint_states.states = [left, right]
        joint_states.nums = 2
        self._robot.move_ee_pos(joint_states)

    def close(self) -> None:
        from .gdk_session import release_gdk

        release_gdk()
