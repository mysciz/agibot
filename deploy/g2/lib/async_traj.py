"""把一块归一化 Δθ 插成 100Hz 伺服要跟的位置点。"""

from __future__ import annotations

import numpy as np

from .actions import decode_normalized_delta, delta_scales
from .joints import ACTION_DIM, JointLayout
from .safety import SafetyConfig, limit_target
from .speed import SpeedConfig, angles_to_velocities


def ticks_per_step(step_duration: float, dt: float) -> int:
    if step_duration <= 0 or dt <= 0:
        raise ValueError("步长和伺服周期必须为正")
    return max(1, int(round(step_duration / dt)))


def samples_between(start: np.ndarray, end: np.ndarray, ticks: int) -> np.ndarray:
    """从 start 走向 end，不含 start，最后一点就是 end。"""
    if ticks < 1:
        raise ValueError("ticks 至少为 1")
    start = np.asarray(start, dtype=np.float64)
    end = np.asarray(end, dtype=np.float64)
    alpha = np.linspace(1.0 / ticks, 1.0, ticks, dtype=np.float64)
    return start + alpha[:, None] * (end - start)


def plan_chunk(
    anchor: np.ndarray,
    actions_norm: np.ndarray,
    layout: JointLayout,
    safety: SafetyConfig,
    speed: SpeedConfig,
    dt: float,
) -> np.ndarray:
    """一块动作变成伺服点。下一块从这一块的最后一个点接着走。"""
    actions = np.asarray(actions_norm, dtype=np.float64)
    if actions.size == 0:
        return np.zeros((0, ACTION_DIM), dtype=np.float64)
    if actions.ndim != 2 or actions.shape[1] != ACTION_DIM:
        raise ValueError(f"动作应为 (N, {ACTION_DIM})")
    pose = np.asarray(anchor, dtype=np.float64).copy()
    if pose.shape != (ACTION_DIM,):
        raise ValueError(f"锚点长度应为 {ACTION_DIM}")
    ticks = ticks_per_step(speed.step_duration, dt)
    scales = delta_scales(safety)
    pieces = []
    for action in actions:
        requested = decode_normalized_delta(action, scales)
        _, stepped = angles_to_velocities(requested, speed)
        limited = limit_target(pose, pose + stepped, layout.limits, safety)
        pieces.append(samples_between(pose, limited.command, ticks))
        pose = limited.command
    return np.concatenate(pieces, axis=0)


def playback_holds(chunk_ticks: list[int], delay_ticks: int, lead_ticks: int) -> tuple[int, int]:
    """按拍模拟播放。返回 (第一块到来前的等待, 中途缓冲区空掉的拍数)。"""
    if delay_ticks < 0 or lead_ticks < 0:
        raise ValueError("延迟和提前量不能为负")
    queue = 0
    pending: int | None = None
    index = 0
    started = False
    opening = 0
    gaps = 0
    guard = 0
    limit = delay_ticks + sum(chunk_ticks) + delay_ticks * (len(chunk_ticks) + 2) + 5
    while guard <= limit:
        guard += 1
        if pending is None and index < len(chunk_ticks) and queue <= lead_ticks:
            pending = delay_ticks
        if pending is not None:
            if pending == 0:
                queue += chunk_ticks[index]
                index += 1
                pending = None
            else:
                pending -= 1
        if queue > 0:
            queue -= 1
            started = True
            continue
        if started and index >= len(chunk_ticks) and pending is None:
            break
        if started:
            gaps += 1
        else:
            opening += 1
        if index >= len(chunk_ticks) and pending is None:
            break
    return opening, gaps
