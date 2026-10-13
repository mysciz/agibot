"""端口 B 的串行循环：读机器人，把观测 POST 到 A，再 GET Δθ 并执行。"""

from __future__ import annotations

import numpy as np

from deploy.g2.lib.camera import prepare_image
from deploy.g2.lib.execution import StepRecord, execute_delta
from deploy.g2.lib.joints import JointLayout, normalize
from deploy.g2.lib.model_client import get_actions, get_health, post_observation
from deploy.g2.lib.safety import SafetyConfig


def run_serial(
    robot,
    cameras,
    model_url: str,
    layout: JointLayout,
    safety: SafetyConfig,
    *,
    task: str = "agibot dual arm",
    max_steps: int = 10,
    open_loop_horizon: int = 1,
    image_height: int = 224,
    image_width: int = 224,
    timeout: float = 120.0,
    verbose: bool = True,
    status_robot=None,
    on_step=None,
) -> list[StepRecord]:
    if max_steps < 1:
        raise ValueError("max_steps 至少为 1")
    if open_loop_horizon < 1:
        raise ValueError("open_loop_horizon 至少为 1")

    health = get_health(model_url, timeout=min(timeout, 5.0))
    if health.get("action_space") != "normalized_delta":
        raise RuntimeError(f"模型端口动作空间不是 normalized_delta: {health.get('action_space')}")
    if verbose:
        print(
            f"[B] 模型 {health.get('source')}  "
            f"scale_j0={health['delta_scale_rad'][0]:.3f} rad",
            flush=True,
        )

    records: list[StepRecord] = []
    while len(records) < max_steps:
        frames = {
            name: prepare_image(image, image_height, image_width)
            for name, image in cameras.read().items()
        }
        proprio_rad = np.asarray(robot.read_radians(), dtype=np.float64)
        proprio_norm = normalize(proprio_rad, layout.limits)
        post_observation(
            model_url, frames, proprio_norm, proprio_rad, task, timeout=min(timeout, 30.0)
        )
        count = min(open_loop_horizon, max_steps - len(records))
        actions, done = get_actions(model_url, count, timeout=timeout)
        if len(actions) == 0:
            if verbose:
                print("[B] 动作已用完", flush=True)
            break

        for action in actions:
            record = execute_delta(robot, action, layout, safety, status_robot=status_robot)
            records.append(record)
            if on_step is not None:
                on_step(record, len(records))
            if verbose:
                print(
                    f"[B] step {len(records)} "
                    f"d0={record.delta_rad[0]:+.4f} rad  "
                    f"cmd0={record.command[0]:+.4f}  limited={record.limited}",
                    flush=True,
                )
            if len(records) >= max_steps:
                break
        if done:
            break
    return records
