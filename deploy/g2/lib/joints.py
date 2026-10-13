"""G2 双臂 + 双夹爪的关节顺序与限位。

下标:
    0:7   左臂 idx21_arm_l_joint1 .. idx27_arm_l_joint7
    7:14  右臂 idx61_arm_r_joint1 .. idx67_arm_r_joint7
    14    左夹爪
    15    右夹爪

这里的 [0, 1] 只用于描述当前关节在限位里的位置（观测）。
模型动作是归一化的 Δθ，换算在 actions.py：0.5 表示不变。

夹爪物理下界是打开，上界是闭合。正的 Δθ 让关节值变大，对 omnipicker 来说是在闭合。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

ACTION_DIM = 16
ARM_DOF = 14

LEFT_ARM = (
    "idx21_arm_l_joint1",
    "idx22_arm_l_joint2",
    "idx23_arm_l_joint3",
    "idx24_arm_l_joint4",
    "idx25_arm_l_joint5",
    "idx26_arm_l_joint6",
    "idx27_arm_l_joint7",
)
RIGHT_ARM = (
    "idx61_arm_r_joint1",
    "idx62_arm_r_joint2",
    "idx63_arm_r_joint3",
    "idx64_arm_r_joint4",
    "idx65_arm_r_joint5",
    "idx66_arm_r_joint6",
    "idx67_arm_r_joint7",
)
ARM_NAMES = LEFT_ARM + RIGHT_ARM

# 单位：弧度。来源：GDK Python robot.md 关节限位表。
ARM_LIMITS = np.array(
    [
        [-3.071796, 3.071796],
        [-2.059505, 2.059505],
        [-3.071796, 3.071796],
        [-2.495838, 1.012308],
        [-3.071796, 3.071796],
        [-1.012308, 1.012308],
        [-1.535907, 1.535907],
        [-3.071796, 3.071796],
        [-2.059505, 2.059505],
        [-3.071796, 3.071796],
        [-2.495838, 1.012308],
        [-3.071796, 3.071796],
        [-1.012308, 1.012308],
        [-1.535907, 1.535907],
    ],
    dtype=np.float64,
)

# 左、右夹爪使用同一组限位。0=打开（下界），1=闭合（上界）。
GRIPPER_LIMITS = {
    "omnipicker": (-0.785, 0.0),
    "dahuan": (0.0, 0.025),
    "ctek90d": (-0.91, 0.0),
}

LEFT_GRIPPER = "idx31_gripper_l_inner_joint1"
RIGHT_GRIPPER = "idx71_gripper_r_inner_joint1"


@dataclass(frozen=True)
class JointLayout:
    gripper_type: str
    names: tuple[str, ...]
    limits: np.ndarray  # (16, 2) 弧度或夹爪行程

    @property
    def action_dim(self) -> int:
        return int(self.limits.shape[0])


def make_layout(gripper_type: str = "omnipicker") -> JointLayout:
    key = gripper_type.strip().lower()
    if key not in GRIPPER_LIMITS:
        known = ", ".join(sorted(GRIPPER_LIMITS))
        raise ValueError(f"未知夹爪类型 {gripper_type!r}，可选: {known}")
    grip = GRIPPER_LIMITS[key]
    limits = np.vstack([ARM_LIMITS, [grip, grip]]).astype(np.float64)
    names = ARM_NAMES + (LEFT_GRIPPER, RIGHT_GRIPPER)
    return JointLayout(gripper_type=key, names=names, limits=limits)


def normalize(radians: np.ndarray, limits: np.ndarray) -> np.ndarray:
    """物理量 -> [0, 1]。越界值会被裁到 0 或 1。"""
    values = np.asarray(radians, dtype=np.float64)
    bounds = np.asarray(limits, dtype=np.float64)
    if values.shape != (bounds.shape[0],):
        raise ValueError(f"关节向量长度应为 {bounds.shape[0]}，实际 {values.shape}")
    span = np.maximum(bounds[:, 1] - bounds[:, 0], 1e-12)
    norm = (values - bounds[:, 0]) / span
    return np.clip(norm, 0.0, 1.0)


def denormalize(norm: np.ndarray, limits: np.ndarray) -> np.ndarray:
    """[0, 1] -> 物理量。输入先裁到 [0, 1]，输出因此落在限位内。"""
    values = np.asarray(norm, dtype=np.float64)
    bounds = np.asarray(limits, dtype=np.float64)
    if values.shape != (bounds.shape[0],):
        raise ValueError(f"动作长度应为 {bounds.shape[0]}，实际 {values.shape}")
    if not np.all(np.isfinite(values)):
        raise ValueError("动作含有 NaN 或 Inf")
    unit = np.clip(values, 0.0, 1.0)
    return bounds[:, 0] + unit * (bounds[:, 1] - bounds[:, 0])
