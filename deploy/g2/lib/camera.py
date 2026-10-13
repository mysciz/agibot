"""相机：内存假图，以及 GDK 彩色相机。模型侧统一为 RGB uint8。"""

from __future__ import annotations

import numpy as np

# 与 GDK CameraType 名称对应。默认三路：头、左手、右手。
CAMERA_TYPE_NAMES = {
    "head": "kHeadColor",
    "left_wrist": "kHandLeftColor",
    "right_wrist": "kHandRightColor",
}


def resize_nearest(image: np.ndarray, height: int, width: int) -> np.ndarray:
    array = np.asarray(image)
    if array.ndim == 2:
        array = np.repeat(array[:, :, None], 3, axis=2)
    if array.shape[-1] > 3:
        array = array[:, :, :3]
    src_h, src_w = array.shape[:2]
    if src_h == height and src_w == width:
        return np.ascontiguousarray(array, dtype=np.uint8)
    rows = np.linspace(0, src_h, height, endpoint=False).astype(np.int64)
    cols = np.linspace(0, src_w, width, endpoint=False).astype(np.int64)
    return np.ascontiguousarray(array[rows][:, cols], dtype=np.uint8)


def prepare_image(image: np.ndarray, height: int, width: int) -> np.ndarray:
    rgb = resize_nearest(image, height, width)
    if rgb.shape != (height, width, 3) or rgb.dtype != np.uint8:
        raise ValueError(f"图像应为 uint8 {(height, width, 3)}，实际 {rgb.dtype} {rgb.shape}")
    return rgb


class MockCameras:
    def __init__(self, height: int = 224, width: int = 224):
        self.height = height
        self.width = width
        self._fills = {"head": 20, "left_wrist": 80, "right_wrist": 160}

    def read(self) -> dict[str, np.ndarray]:
        frames = {}
        for name, fill in self._fills.items():
            frames[name] = np.full((self.height, self.width, 3), fill, dtype=np.uint8)
        return frames

    def close(self) -> None:
        return None


def _as_uint8_buffer(data) -> np.ndarray:
    if isinstance(data, (bytes, bytearray)):
        return np.frombuffer(data, dtype=np.uint8)
    array = np.asarray(data)
    if array.dtype != np.uint8:
        array = array.view(np.uint8) if array.itemsize == 1 else np.asarray(array, dtype=np.uint8)
    return np.ascontiguousarray(array, dtype=np.uint8).ravel()


def _looks_like_jpeg(encoding, buffer: np.ndarray) -> bool:
    name = str(encoding).upper()
    if "JPEG" in name or "JPG" in name:
        return True
    return buffer.size >= 2 and int(buffer[0]) == 0xFF and int(buffer[1]) == 0xD8


def decode_gdk_image(image) -> np.ndarray:
    """把 GDK Image 解成 RGB uint8。JPEG 经 OpenCV 解码后从 BGR 转回 RGB。"""
    if image is None or not hasattr(image, "data"):
        raise RuntimeError("相机没有返回图像")
    buffer = _as_uint8_buffer(image.data)
    if buffer.size == 0:
        raise RuntimeError("相机图像为空")

    encoding = getattr(image, "encoding", "")
    if _looks_like_jpeg(encoding, buffer) or "PNG" in str(encoding).upper():
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError("解码 JPEG/PNG 需要 opencv-python") from exc
        decoded = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        if decoded is None:
            raise RuntimeError(f"图像解码失败: encoding={encoding}")
        return np.ascontiguousarray(decoded[:, :, ::-1])

    height = int(image.height)
    width = int(image.width)
    color = str(getattr(image, "color_format", "")).upper()
    if "GRAY" in color:
        gray = buffer.reshape((height, width))
        return np.repeat(gray[:, :, None], 3, axis=2)
    channels = 3 if buffer.size == height * width * 3 else 1
    if channels == 1:
        gray = buffer.reshape((height, width))
        return np.repeat(gray[:, :, None], 3, axis=2)
    rgb = buffer.reshape((height, width, 3))
    if "BGR" in color and "RGB" not in color:
        rgb = rgb[:, :, ::-1]
    return np.ascontiguousarray(rgb)


class GdkCameras:
    def __init__(self, names: tuple[str, ...] = ("head", "left_wrist", "right_wrist"), timeout_ms: float = 1000.0):
        from .gdk_session import ensure_gdk

        unknown = [name for name in names if name not in CAMERA_TYPE_NAMES]
        if unknown:
            raise ValueError(f"未知相机 {unknown}，可选 {sorted(CAMERA_TYPE_NAMES)}")
        self._gdk = ensure_gdk()
        self._camera = self._gdk.Camera()
        self._names = tuple(names)
        self._timeout_ms = float(timeout_ms)
        self._types = {}
        for name in self._names:
            type_name = CAMERA_TYPE_NAMES[name]
            self._types[name] = getattr(self._gdk.CameraType, type_name)

    def read(self) -> dict[str, np.ndarray]:
        frames = {}
        for name, camera_type in self._types.items():
            image = self._camera.get_latest_image(camera_type, self._timeout_ms)
            frames[name] = decode_gdk_image(image)
        return frames

    def close(self) -> None:
        closer = getattr(self._camera, "close", None)
        if callable(closer):
            closer()
