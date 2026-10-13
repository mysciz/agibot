"""用文件或终端代替 WAM。输出始终是归一化 Δθ。"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .actions import encode_delta_rad
from .joints import ACTION_DIM


def _as_steps(array: np.ndarray) -> np.ndarray:
    steps = np.asarray(array, dtype=np.float64)
    if steps.ndim == 1:
        steps = steps.reshape(1, -1)
    if steps.ndim != 2 or steps.shape[1] != ACTION_DIM:
        raise ValueError(f"动作应为 (T, {ACTION_DIM})，实际 {steps.shape}")
    if not np.all(np.isfinite(steps)):
        raise ValueError("动作文件含有 NaN 或 Inf")
    return steps


def load_steps(path: str | Path, scales: np.ndarray) -> np.ndarray:
    """读取 JSON，返回 (T, 16) 的归一化 Δθ。

    unit=rad：文件里是弧度增量，按 scale 编成 0-1。
    unit=norm：文件里已经是 0-1，0.5 为不动。
    支持 "steps" 或 "chunks"（按顺序拼平）。
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    unit = str(payload.get("unit", "rad")).lower()
    if "steps" in payload:
        raw = _as_steps(payload["steps"])
    elif "chunks" in payload:
        rows = []
        for chunk in payload["chunks"]:
            rows.append(_as_steps(chunk))
        if not rows:
            raise ValueError("chunks 为空")
        raw = np.concatenate(rows, axis=0)
    else:
        raise ValueError("动作文件需要 steps 或 chunks")

    if unit == "norm":
        return np.clip(raw, 0.0, 1.0)
    if unit == "rad":
        return np.stack([encode_delta_rad(row, scales) for row in raw], axis=0)
    raise ValueError(f"未知 unit {unit!r}，用 rad 或 norm")


def parse_command(line: str, scales: np.ndarray) -> np.ndarray | None:
    """解析终端一行。quit 返回 None。hold 或空行是全 0.5。"""
    text = line.strip()
    if text in {"q", "quit", "done"}:
        return None
    if text == "" or text == "hold":
        return np.full(ACTION_DIM, 0.5, dtype=np.float64)

    parts = text.split()
    kind = "rad"
    if parts[0] in {"rad", "norm"}:
        kind = parts[0]
        parts = parts[1:]
    if len(parts) != ACTION_DIM:
        raise ValueError(f"需要 {ACTION_DIM} 个数，实际 {len(parts)}。示例: rad 0.05 0 0 ...")
    values = np.array([float(item) for item in parts], dtype=np.float64)
    if kind == "norm":
        return np.clip(values, 0.0, 1.0)
    return encode_delta_rad(values, scales)


class FileSource:
    def __init__(self, steps: np.ndarray):
        self.steps = _as_steps(steps)
        self.index = 0

    @property
    def remaining(self) -> int:
        return int(self.steps.shape[0] - self.index)

    def take(self, count: int) -> tuple[np.ndarray, bool]:
        if count < 1:
            raise ValueError("count 至少为 1")
        if self.index >= self.steps.shape[0]:
            return np.zeros((0, ACTION_DIM), dtype=np.float64), True
        end = min(self.index + count, self.steps.shape[0])
        chunk = self.steps[self.index:end].copy()
        self.index = end
        return chunk, self.index >= self.steps.shape[0]


class StdinSource:
    """每次 take 向终端要 count 行。一行是一个时间步。"""

    def __init__(self, scales: np.ndarray, input_fn=input, output_fn=print):
        self.scales = np.asarray(scales, dtype=np.float64)
        self._input = input_fn
        self._output = output_fn
        self._closed = False

    @property
    def remaining(self) -> int:
        return 0 if self._closed else -1

    def take(self, count: int) -> tuple[np.ndarray, bool]:
        if self._closed:
            return np.zeros((0, ACTION_DIM), dtype=np.float64), True
        rows = []
        for _ in range(count):
            self._output(
                "Δθ>  16 个数，默认弧度；或 `norm ...` / `hold` / `quit`",
                flush=True,
            )
            line = self._input()
            if line is None:
                self._closed = True
                break
            parsed = parse_command(line, self.scales)
            if parsed is None:
                self._closed = True
                break
            rows.append(parsed)
        if not rows:
            return np.zeros((0, ACTION_DIM), dtype=np.float64), True
        return np.stack(rows, axis=0), self._closed
