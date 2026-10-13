#!/usr/bin/env python3
"""左腕末关节 idx27_arm_l_joint7 转 0.05 rad，再转回。

    python deploy/examples/nudge_left_wrist.py
    python deploy/examples/nudge_left_wrist.py --delta 0.03
"""

from nudge_wrist import main

if __name__ == "__main__":
    main("left")
