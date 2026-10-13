"""归一化 Δθ 与弧度增量互转。

线上每个数都在 [0, 1]：
    0.5 -> 0 rad
    0   -> -scale
    1   -> +scale
scale 按关节给：手臂用 max_joint_step_rad，夹爪用 max_gripper_step。
正增量表示该关节的物理量变大。omnipicker 变大是闭合。
"""

from __future__ import annotations

import numpy as np

from .joints import ACTION_DIM, ARM_DOF
from .safety import SafetyConfig


def delta_scales(config: SafetyConfig) -> np.ndarray:
    scales = np.full(ACTION_DIM, float(config.max_joint_step_rad), dtype=np.float64)
    scales[ARM_DOF:] = float(config.max_gripper_step)
    return scales


def decode_normalized_delta(unit: np.ndarray, scales: np.ndarray) -> np.ndarray:
    """[0, 1] 的 Δθ -> 弧度（或夹爪行程）增量。"""
    values = np.asarray(unit, dtype=np.float64).reshape(-1)
    span = np.asarray(scales, dtype=np.float64).reshape(-1)
    if values.shape != (ACTION_DIM,) or span.shape != (ACTION_DIM,):
        raise ValueError(f"Δθ 长度应为 {ACTION_DIM}")
    if not np.all(np.isfinite(values)):
        raise ValueError("Δθ 含有 NaN 或 Inf")
    clipped = np.clip(values, 0.0, 1.0)
    return (clipped - 0.5) * 2.0 * span


def encode_delta_rad(delta_rad: np.ndarray, scales: np.ndarray) -> np.ndarray:
    """弧度增量 -> [0, 1]。超出 ±scale 的部分会被裁掉。"""
    delta = np.asarray(delta_rad, dtype=np.float64).reshape(-1)
    span = np.maximum(np.asarray(scales, dtype=np.float64).reshape(-1), 1e-12)
    if delta.shape != (ACTION_DIM,):
        raise ValueError(f"Δθ 长度应为 {ACTION_DIM}，实际 {delta.shape}")
    if not np.all(np.isfinite(delta)):
        raise ValueError("Δθ 含有 NaN 或 Inf")
    limited = np.clip(delta, -span, span)
    return 0.5 + limited / (2.0 * span)
