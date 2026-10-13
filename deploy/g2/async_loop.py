"""端口 B 的异步循环：播放不停止，下一块在缓冲区快空时去要。"""

from __future__ import annotations

import threading
import time

import numpy as np

from deploy.g2.lib.async_traj import plan_chunk
from deploy.g2.lib.camera import prepare_image
from deploy.g2.lib.command_buffer import CommandBuffer
from deploy.g2.lib.joints import JointLayout, normalize
from deploy.g2.lib.model_client import get_actions, get_health, post_observation
from deploy.g2.lib.safety import SafetyConfig, check_status
from deploy.g2.lib.speed import SpeedConfig


class AsyncResult:
    def __init__(self, steps: int, sent: int, holds: int):
        self.steps = steps
        self.sent = sent
        self.holds = holds


def run_async(
    robot,
    cameras,
    model_url: str,
    layout: JointLayout,
    safety: SafetyConfig,
    speed: SpeedConfig,
    *,
    task: str = "agibot dual arm",
    max_steps: int = 10,
    open_loop_horizon: int = 4,
    infer_delay: float = 0.0,
    prefetch_margin: float = 0.05,
    servo_hz: float = 100.0,
    control_period: float = 0.0,
    image_height: int = 224,
    image_width: int = 224,
    timeout: float = 120.0,
    verbose: bool = True,
    status_robot=None,
    on_chunk=None,
) -> AsyncResult:
    if max_steps < 1:
        raise ValueError("max_steps 至少为 1")
    if open_loop_horizon < 1:
        raise ValueError("open_loop_horizon 至少为 1")
    if servo_hz <= 0:
        raise ValueError("servo_hz 必须为正")
    if infer_delay < 0 or prefetch_margin < 0:
        raise ValueError("推理延迟和提前量不能为负")
    dt = 1.0 / servo_hz
    period = control_period if control_period > 0 else dt * 1.2
    lead = infer_delay + prefetch_margin

    health = get_health(model_url, timeout=min(timeout, 5.0))
    if health.get("action_space") != "normalized_delta":
        raise RuntimeError(f"模型端口动作空间不是 normalized_delta: {health.get('action_space')}")
    if verbose:
        print(
            f"[B] 模型 {health.get('source')}  "
            f"chunk={open_loop_horizon}  step={speed.step_duration:.2f}s  "
            f"infer={infer_delay:.2f}s  servo={servo_hz:.0f}Hz",
            flush=True,
        )

    buffer = CommandBuffer(robot.read_radians())
    stop = threading.Event()
    chunks_done = threading.Event()
    player_error: list[BaseException] = []
    watcher = status_robot or robot

    def _play() -> None:
        tick = 0
        next_tick = time.monotonic()
        try:
            while not stop.is_set():
                if buffer.remaining() == 0 and chunks_done.is_set():
                    break
                if tick % 10 == 0:
                    check_status(watcher.read_status())
                point, _holding = buffer.pop()
                robot.servo_joints(point, period)
                tick += 1
                next_tick += dt
                pause = next_tick - time.monotonic()
                if pause > 0:
                    time.sleep(pause)
                else:
                    next_tick = time.monotonic()
        except BaseException as exc:  # noqa: BLE001
            player_error.append(exc)
            stop.set()

    player = threading.Thread(target=_play, name="servo-player", daemon=True)
    player.start()
    taken = 0
    try:
        while taken < max_steps and not stop.is_set():
            while buffer.remaining() * dt > lead and not stop.is_set():
                time.sleep(dt)
            if stop.is_set() or taken >= max_steps:
                break
            frames = {
                name: prepare_image(image, image_height, image_width)
                for name, image in cameras.read().items()
            }
            measured = np.asarray(robot.read_radians(), dtype=np.float64)
            post_observation(
                model_url,
                frames,
                normalize(measured, layout.limits),
                measured,
                task,
                timeout=min(timeout, 30.0),
            )
            count = min(open_loop_horizon, max_steps - taken)
            actions, done = get_actions(model_url, count, timeout=timeout)
            if len(actions) == 0:
                if verbose:
                    print("[B] 动作已用完", flush=True)
                break
            samples = plan_chunk(buffer.anchor(), actions, layout, safety, speed, dt)
            buffer.append(samples)
            taken += len(actions)
            if on_chunk is not None:
                on_chunk(taken, len(samples))
            if verbose:
                print(
                    f"[B] chunk steps={taken}  samples=+{len(samples)}  "
                    f"queued={buffer.remaining() * dt:.2f}s",
                    flush=True,
                )
            if done:
                break
    finally:
        chunks_done.set()
        deadline = time.monotonic() + max(timeout, 1.0)
        while buffer.remaining() > 0 and not stop.is_set() and time.monotonic() < deadline:
            time.sleep(dt)
        stop.set()
        player.join(timeout=2.0)
    if player_error:
        raise player_error[0]
    return AsyncResult(steps=taken, sent=buffer.sent, holds=buffer.holds)
