"""伺服播放用的位置队列。空的时候重复最后一个点。"""

from __future__ import annotations

import threading
from collections import deque

import numpy as np

from .joints import ACTION_DIM


class CommandBuffer:
    def __init__(self, initial: np.ndarray):
        pose = np.asarray(initial, dtype=np.float64)
        if pose.shape != (ACTION_DIM,):
            raise ValueError(f"初始姿态长度应为 {ACTION_DIM}")
        self._lock = threading.Lock()
        self._queue: deque[np.ndarray] = deque()
        self._last = pose.copy()
        self.holds = 0
        self.sent = 0

    def anchor(self) -> np.ndarray:
        with self._lock:
            if self._queue:
                return self._queue[-1].copy()
            return self._last.copy()

    def append(self, samples: np.ndarray) -> None:
        rows = np.asarray(samples, dtype=np.float64)
        if rows.size == 0:
            return
        if rows.ndim != 2 or rows.shape[1] != ACTION_DIM:
            raise ValueError(f"伺服点应为 (N, {ACTION_DIM})")
        with self._lock:
            for row in rows:
                self._queue.append(row.copy())

    def remaining(self) -> int:
        with self._lock:
            return len(self._queue)

    def pop(self) -> tuple[np.ndarray, bool]:
        with self._lock:
            if self._queue:
                self._last = self._queue.popleft()
                self.sent += 1
                return self._last.copy(), False
            self.holds += 1
            return self._last.copy(), True
