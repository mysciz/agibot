"""把一步归一化 Δθ 加到当前关节角上，限制后再阻塞执行。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .actions import decode_normalized_delta, delta_scales
from .joints import ARM_DOF, JointLayout
from .safety import LimitResult, SafetyConfig, check_status, limit_target
from .speed import SpeedConfig, angles_to_velocities


@dataclass
class StepRecord:
    proprio_rad: np.ndarray
    action_norm: np.ndarray
    delta_rad: np.ndarray
    command: np.ndarray
    limited: bool
    velocity: np.ndarray | None = None


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


def execute_speed(
    robot,
    action_norm: np.ndarray,
    layout: JointLayout,
    safety: SafetyConfig,
    speed: SpeedConfig,
    status_robot=None,
) -> StepRecord:
    """Δθ 先变成速度，再乘时间得到这一步的目标角度。仍等 move_arm_joint 返回。"""
    check_status((status_robot or robot).read_status())
    current = np.asarray(robot.read_radians(), dtype=np.float64)
    requested = decode_normalized_delta(action_norm, delta_scales(safety))
    _, stepped = angles_to_velocities(requested, speed)
    limited = limit_target(current, current + stepped, layout.limits, safety)
    command = limited.command
    velocity = (command - current) / speed.step_duration

    arm_delta = float(np.max(np.abs(command[:ARM_DOF] - current[:ARM_DOF])))
    if arm_delta > safety.position_tolerance:
        arm_speed = np.maximum(np.abs(velocity[:ARM_DOF]), speed.min_velocity)
        robot.move_arms(command[:ARM_DOF], arm_speed)

    grip_delta = float(np.max(np.abs(command[ARM_DOF:] - current[ARM_DOF:])))
    if grip_delta > safety.position_tolerance:
        robot.move_grippers(command[ARM_DOF:])

    return StepRecord(
        proprio_rad=current,
        action_norm=np.asarray(action_norm, dtype=np.float64).copy(),
        delta_rad=requested,
        command=command.copy(),
        limited=limited.limited or not np.allclose(stepped, requested, atol=1e-8),
        velocity=velocity,
    )
