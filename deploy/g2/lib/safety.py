"""下发前的限制策略。

串行模式走 GDK 的阻塞规划接口（move_arm_joint），不走 100Hz 伺服。
在此之上再加四层限制，避免单步指令把关节打到限位外或一次跳太远：

1. 归一化 Δθ 先裁到 [0, 1]，再换成相对当前姿态的弧度增量
2. 手臂目标再向限位内收一个 margin
3. 相对当前角度的单步变化不超过 max_joint_step_rad
4. 急停或错误码非 0 时拒绝下发
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .joints import ARM_DOF


class SafetyStop(RuntimeError):
    """机器人状态不允许继续发运动指令。"""


@dataclass
class SafetyConfig:
    max_joint_step_rad: float = 0.10
    max_gripper_step: float = 0.30
    limit_margin_rad: float = 0.02
    joint_velocity: float = 0.20
    position_tolerance: float = 1e-3

    def __post_init__(self) -> None:
        if self.max_joint_step_rad <= 0:
            raise ValueError("max_joint_step_rad 必须为正")
        if self.max_gripper_step <= 0:
            raise ValueError("max_gripper_step 必须为正")
        if self.limit_margin_rad < 0:
            raise ValueError("limit_margin_rad 不能为负")
        if self.joint_velocity <= 0:
            raise ValueError("joint_velocity 必须为正")


@dataclass
class LimitResult:
    command: np.ndarray
    target: np.ndarray
    limited: bool


def check_status(status: dict) -> None:
    estop_keys = ("left_arm_estop", "right_arm_estop")
    for key in estop_keys:
        if status.get(key):
            raise SafetyStop(f"{key} 为真，已停止下发")
    error_keys = (
        "left_arm_error",
        "right_arm_error",
        "left_end_error",
        "right_end_error",
    )
    for key in error_keys:
        code = int(status.get(key, 0) or 0)
        if code != 0:
            raise SafetyStop(f"{key}={code}，已停止下发")


def _effective_limits(limits: np.ndarray, margin: float) -> np.ndarray:
    bounds = np.array(limits, dtype=np.float64, copy=True)
    if margin <= 0:
        return bounds
    span = bounds[:ARM_DOF, 1] - bounds[:ARM_DOF, 0]
    shrink = span > (2.0 * margin)
    bounds[:ARM_DOF, 0] = np.where(shrink, bounds[:ARM_DOF, 0] + margin, bounds[:ARM_DOF, 0])
    bounds[:ARM_DOF, 1] = np.where(shrink, bounds[:ARM_DOF, 1] - margin, bounds[:ARM_DOF, 1])
    return bounds


def limit_target(
    current: np.ndarray,
    target: np.ndarray,
    limits: np.ndarray,
    config: SafetyConfig,
) -> LimitResult:
    """把绝对目标限制在限位内，并限制相对当前姿态的单步位移。"""
    current = np.asarray(current, dtype=np.float64)
    target = np.asarray(target, dtype=np.float64)
    if current.shape != target.shape:
        raise ValueError(f"当前姿态 {current.shape} 与目标 {target.shape} 不一致")
    if not np.all(np.isfinite(current)) or not np.all(np.isfinite(target)):
        raise ValueError("姿态含有 NaN 或 Inf")

    bounds = _effective_limits(limits, config.limit_margin_rad)
    clipped = np.clip(target, bounds[:, 0], bounds[:, 1])

    max_step = np.full(current.shape, config.max_joint_step_rad, dtype=np.float64)
    max_step[ARM_DOF:] = config.max_gripper_step
    delta = np.clip(clipped - current, -max_step, max_step)
    command = np.clip(current + delta, bounds[:, 0], bounds[:, 1])
    limited = not np.allclose(command, target, atol=1e-8)
    return LimitResult(command=command, target=target, limited=limited)
