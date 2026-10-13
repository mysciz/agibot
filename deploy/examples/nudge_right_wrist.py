#!/usr/bin/env python3
"""右腕末关节 idx67_arm_r_joint7 转 0.05 rad，再转回。

    python deploy/examples/nudge_right_wrist.py
    python deploy/examples/nudge_right_wrist.py --delta 0.03
"""

from nudge_wrist import main

if __name__ == "__main__":
    main("right")
