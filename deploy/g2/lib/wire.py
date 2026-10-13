"""观测里的图像用 base64 原始字节传输，避免把 uint8 展开成 JSON 数字。

动作块很短，仍用普通 JSON 数组，方便直接查看。
"""

from __future__ import annotations

import base64

import numpy as np

WIRE_KEY = "__b64__"
WIRE_VERSION = 1


def encode_array(arr: np.ndarray) -> dict:
    array = np.ascontiguousarray(arr)
    return {
        WIRE_KEY: WIRE_VERSION,
        "dtype": str(array.dtype),
        "shape": list(array.shape),
        "data": base64.b64encode(array.tobytes()).decode("ascii"),
    }


def decode_array(obj, dtype=None) -> np.ndarray:
    if not isinstance(obj, dict) or WIRE_KEY not in obj:
        array = np.array(obj, dtype=dtype) if dtype else np.array(obj)
        return array

    version = obj.get(WIRE_KEY)
    if version != WIRE_VERSION:
        raise ValueError(f"不支持的 wire 版本 {version!r}")

    shape = tuple(int(x) for x in obj["shape"])
    wire_dtype = np.dtype(obj["dtype"])
    buffer = base64.b64decode(obj["data"])
    expected = int(np.prod(shape)) * wire_dtype.itemsize if shape else wire_dtype.itemsize
    if len(buffer) != expected:
        raise ValueError(
            f"字节长度不符: 收到 {len(buffer)}，期望 {expected}，shape={shape} dtype={wire_dtype}"
        )
    array = np.frombuffer(buffer, dtype=wire_dtype).reshape(shape).copy()
    if dtype is not None and array.dtype != np.dtype(dtype):
        array = array.astype(dtype, copy=False)
    return array
