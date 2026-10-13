"""读当前双臂角度，把一侧手腕末关节转一个小角度，再转回去。"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deploy.g2.lib.joints import ARM_NAMES, make_layout
from deploy.g2.lib.robot import GdkRobot
from deploy.g2.lib.safety import check_status

# 手臂向量下标：左腕 idx27 是 6，右腕 idx67 是 13。
WRIST = {
    "left": 6,
    "right": 13,
}
MAX_ABS_DELTA = 0.15
LIMIT_MARGIN = 0.02
VELOCITY = 0.2


def nudge(arm: str, delta: float, velocity: float = VELOCITY) -> None:
    if arm not in WRIST:
        raise ValueError("arm 只能是 left 或 right")
    if not np.isfinite(delta) or abs(delta) > MAX_ABS_DELTA:
        raise ValueError(f"delta 绝对值不能超过 {MAX_ABS_DELTA} rad")

    index = WRIST[arm]
    name = ARM_NAMES[index]
    layout = make_layout()
    low = float(layout.limits[index, 0] + LIMIT_MARGIN)
    high = float(layout.limits[index, 1] - LIMIT_MARGIN)

    robot = GdkRobot(layout)
    try:
        check_status(robot.read_status())
        current = robot.read_radians()
        start = float(current[index])
        target = float(np.clip(start + delta, low, high))
        print(f"{name}: {start:+.4f} -> {target:+.4f} rad ({np.degrees(delta):+.1f} deg)")
        print("2 秒后运动，Ctrl+C 取消")
        time.sleep(2)

        pose = current[:14].copy()
        pose[index] = target
        robot.move_arms(pose, velocity)
        print(f"到达 {robot.read_radians()[index]:+.4f} rad，1 秒后回到原位")
        time.sleep(1)

        pose[index] = start
        robot.move_arms(pose, velocity)
        print(f"已回到 {robot.read_radians()[index]:+.4f} rad")
    finally:
        robot.close()


def main(arm: str) -> None:
    parser = argparse.ArgumentParser(description=f"转动{arm}手腕末关节一个小角度，再转回")
    parser.add_argument("--delta", type=float, default=0.05, help="弧度，默认 0.05（约 3 度）")
    args = parser.parse_args()
    nudge(arm, args.delta)


if __name__ == "__main__":
    main("left")
