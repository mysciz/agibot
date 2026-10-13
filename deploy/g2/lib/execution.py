"""把一步归一化 Δθ 加到当前关节角上，限制后再阻塞执行。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .actions import decode_normalized_delta, delta_scales
from .joints import ARM_DOF, JointLayout
from .safety import LimitResult, SafetyConfig, check_status, limit_target


@dataclass
class StepRecord:
    proprio_rad: np.ndarray
    action_norm: np.ndarray
    delta_rad: np.ndarray
    command: np.ndarray
    limited: bool


def execute_delta(
    robot,
    action_norm: np.ndarray,
    layout: JointLayout,
    safety: SafetyConfig,
    status_robot=None,
) -> StepRecord:
    check_status((status_robot or robot).read_status())
    current = np.asarray(robot.read_radians(), dtype=np.float64)
    scales = delta_scales(safety)
    delta = decode_normalized_delta(action_norm, scales)
    limited: LimitResult = limit_target(current, current + delta, layout.limits, safety)
    command = limited.command

    arm_delta = float(np.max(np.abs(command[:ARM_DOF] - current[:ARM_DOF])))
    if arm_delta > safety.position_tolerance:
        robot.move_arms(command[:ARM_DOF], safety.joint_velocity)

    grip_delta = float(np.max(np.abs(command[ARM_DOF:] - current[ARM_DOF:])))
    if grip_delta > safety.position_tolerance:
        robot.move_grippers(command[ARM_DOF:])

    return StepRecord(
        proprio_rad=current,
        action_norm=np.asarray(action_norm, dtype=np.float64).copy(),
        delta_rad=delta,
        command=command.copy(),
        limited=limited.limited,
    )
