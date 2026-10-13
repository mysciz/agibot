"""把 RGB uint8 写成 PNG，不依赖 OpenCV。"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

import numpy as np


def write_rgb_png(path: str | Path, image: np.ndarray) -> None:
    rgb = np.asarray(image)
    if rgb.dtype != np.uint8 or rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError(f"PNG 需要 uint8 HxWx3，实际 {rgb.dtype} {rgb.shape}")
    height, width = rgb.shape[:2]
    raw = b"".join(b"\x00" + np.ascontiguousarray(rgb[row]).tobytes() for row in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    Path(path).write_bytes(png)
