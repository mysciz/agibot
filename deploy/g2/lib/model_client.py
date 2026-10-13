"""机器人侧访问模型端口：POST 观测，GET 动作块。"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

import numpy as np

from .joints import ACTION_DIM
from .wire import encode_array


def get_health(model_url: str, timeout: float = 5.0) -> dict:
    with urllib.request.urlopen(model_url.rstrip("/") + "/health", timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def post_observation(
    model_url: str,
    images: dict[str, np.ndarray],
    proprio_norm: np.ndarray,
    proprio_rad: np.ndarray,
    task: str,
    timeout: float = 30.0,
) -> dict:
    payload = {
        "images": {name: encode_array(image) for name, image in images.items()},
        "proprio": encode_array(np.asarray(proprio_norm, dtype=np.float32)),
        "proprio_rad": encode_array(np.asarray(proprio_rad, dtype=np.float64)),
        "task": task,
    }
    return _request(model_url, "/observation", payload, timeout)


def get_actions(model_url: str, count: int, timeout: float = 120.0) -> tuple[np.ndarray, bool]:
    body = _request(model_url, f"/actions?n={int(count)}", None, timeout, method="GET")
    if body.get("action_space") not in (None, "normalized_delta"):
        raise RuntimeError(f"动作空间不是 normalized_delta: {body.get('action_space')}")
    actions = np.asarray(body.get("actions", []), dtype=np.float64)
    if actions.size == 0:
        return np.zeros((0, ACTION_DIM), dtype=np.float64), True
    if actions.ndim != 2 or actions.shape[1] != ACTION_DIM:
        raise RuntimeError(f"动作形状应为 (N, {ACTION_DIM})，实际 {actions.shape}")
    return actions, bool(body.get("done", False))


def _request(model_url: str, path: str, payload: dict | None, timeout: float, method: str = "POST") -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        model_url.rstrip("/") + path,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"模型端口 {path} 返回 {exc.code}: {detail}") from exc
