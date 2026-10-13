"""把一步转角增量换成关节速度，再积分成这一步要去的角度。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .joints import ACTION_DIM, ARM_DOF


@dataclass
class SpeedConfig:
    step_duration: float = 0.5
    max_joint_vel: float = 0.20
    max_gripper_vel: float = 0.40
    min_velocity: float = 0.02

    def __post_init__(self) -> None:
        if self.step_duration <= 0:
            raise ValueError("step_duration 必须为正")
        if self.max_joint_vel <= 0 or self.max_gripper_vel <= 0:
            raise ValueError("速度上限必须为正")
        if self.min_velocity <= 0:
            raise ValueError("min_velocity 必须为正")


def angles_to_velocities(delta_rad: np.ndarray, config: SpeedConfig) -> tuple[np.ndarray, np.ndarray]:
    """Δθ / T，并限制在速度上限内。

    返回带符号的速度，以及这一步实际允许转过的角度（速度乘时间）。
    """
    delta = np.asarray(delta_rad, dtype=np.float64).reshape(-1)
    if delta.shape != (ACTION_DIM,):
        raise ValueError(f"Δθ 长度应为 {ACTION_DIM}")
    cap = np.full(ACTION_DIM, config.max_joint_vel, dtype=np.float64)
    cap[ARM_DOF:] = config.max_gripper_vel
    velocity = np.clip(delta / config.step_duration, -cap, cap)
    return velocity, velocity * config.step_duration
