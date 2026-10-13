"""端口 A：模型侧。没有 WAM 时，从文件或终端取出归一化 Δθ 动作块。"""

from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import numpy as np

from deploy.g2.lib.action_source import FileSource, StdinSource, load_steps
from deploy.g2.lib.actions import delta_scales
from deploy.g2.lib.joints import ACTION_DIM, make_layout
from deploy.g2.lib.png_rgb import write_rgb_png
from deploy.g2.lib.safety import SafetyConfig
from deploy.g2.lib.wire import decode_array

_REQUIRED_IMAGES = ("head", "left_wrist", "right_wrist")


class ModelState:
    def __init__(
        self,
        source,
        scales: np.ndarray,
        names: tuple[str, ...],
        source_name: str,
        infer_delay: float = 0.0,
        save_dir: str = "",
    ):
        self.source = source
        self.scales = np.asarray(scales, dtype=np.float64)
        self.names = names
        self.source_name = source_name
        self.infer_delay = float(infer_delay)
        self.save_dir = save_dir
        self._lock = threading.Lock()
        self.observations = 0
        self.last_proprio_rad: np.ndarray | None = None


def _health(state: ModelState) -> dict:
    return {
        "role": "model",
        "status": "ok",
        "action_dim": ACTION_DIM,
        "action_space": "normalized_delta",
        "zero_action": 0.5,
        "delta_scale_rad": state.scales.tolist(),
        "action_layout": list(state.names),
        "source": state.source_name,
        "infer_delay_s": state.infer_delay,
        "steps_remaining": state.source.remaining,
        "observations": state.observations,
    }


def _save_observation(folder: Path, frames: dict[str, np.ndarray], proprio_rad: np.ndarray) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for name, image in frames.items():
        write_rgb_png(folder / f"{name}.png", image)
    payload = {"proprio_rad": np.round(proprio_rad, 6).tolist()}
    (folder / "proprio.json").write_text(json.dumps(payload), encoding="utf-8")


def _read_observation(state: ModelState, body: dict) -> None:
    images = body.get("images")
    if not isinstance(images, dict):
        raise ValueError("缺少 images")
    frames: dict[str, np.ndarray] = {}
    for name in _REQUIRED_IMAGES:
        if name not in images:
            raise ValueError(f"缺少图像 {name}")
        image = decode_array(images[name], dtype=np.uint8)
        if image.ndim != 3 or image.shape[-1] != 3:
            raise ValueError(f"{name} 应为 HxWx3，实际 {image.shape}")
        frames[name] = image
    proprio_rad = decode_array(body["proprio_rad"], dtype=np.float64).reshape(-1)
    if proprio_rad.shape != (ACTION_DIM,):
        raise ValueError(f"proprio_rad 长度应为 {ACTION_DIM}")
    with state._lock:
        state.observations += 1
        index = state.observations
        state.last_proprio_rad = proprio_rad
    saved = ""
    if state.save_dir:
        folder = Path(state.save_dir) / f"{index:04d}"
        _save_observation(folder, frames, proprio_rad)
        saved = f"  saved={folder}"
    print(
        f"[A] 观测 #{index} "
        f"j0={proprio_rad[0]:+.4f} rad  "
        f"grip=({proprio_rad[14]:+.4f}, {proprio_rad[15]:+.4f})"
        f"{saved}",
        flush=True,
    )


def make_handler(state: ModelState):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/health":
                self._send(200, _health(state))
                return
            if parsed.path != "/actions":
                self._send(404, {"error": "not found"})
                return
            query = parse_qs(parsed.query)
            try:
                count = int(query.get("n", ["1"])[0])
            except ValueError as exc:
                self._send(400, {"error": str(exc)})
                return
            if state.infer_delay > 0:
                time.sleep(state.infer_delay)
            try:
                chunk, done = state.source.take(count)
            except Exception as exc:  # noqa: BLE001
                self._send(400, {"error": str(exc)})
                return
            print(f"[A] 发出 {len(chunk)} 步 Δθ  done={done}", flush=True)
            self._send(
                200,
                {
                    "actions": chunk.tolist(),
                    "action_space": "normalized_delta",
                    "action_dim": ACTION_DIM,
                    "done": done,
                },
            )

        def do_POST(self):  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path != "/observation":
                self._send(404, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                _read_observation(state, body)
            except Exception as exc:  # noqa: BLE001
                self._send(400, {"error": str(exc)})
                return
            self._send(200, {"ok": True, "observations": state.observations})

        def _send(self, code: int, payload: dict) -> None:
            data = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, fmt: str, *args) -> None:
            print(f"[A] {self.address_string()} {fmt % args}", flush=True)

    return Handler


def serve(state: ModelState, host: str, port: int) -> ThreadingHTTPServer:
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer((host, port), make_handler(state))
    bound_host, bound_port = httpd.server_address[:2]
    print(
        f"[A] 模型端口 http://{bound_host}:{bound_port}  "
        f"source={state.source_name}  infer={state.infer_delay:.2f}s  "
        f"save={state.save_dir or '-'}  Δθ 0.5=不动",
        flush=True,
    )
    return httpd


def build_state(
    source_name: str,
    actions_file: str,
    gripper: str,
    safety: SafetyConfig,
    infer_delay: float = 0.0,
    save_dir: str = "",
) -> ModelState:
    layout = make_layout(gripper)
    scales = delta_scales(safety)
    if source_name == "file":
        steps = load_steps(actions_file, scales)
        source = FileSource(steps)
    elif source_name == "stdin":
        source = StdinSource(scales)
    else:
        raise ValueError("source 只能是 file 或 stdin")
    return ModelState(
        source, scales, layout.names, source_name, infer_delay=infer_delay, save_dir=save_dir
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="端口 A：用文件或终端代替 WAM")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8800)
    parser.add_argument("--source", choices=["file", "stdin"], default="file")
    parser.add_argument("--actions", default="")
    parser.add_argument("--gripper", default="omnipicker")
    parser.add_argument("--max-joint-step", type=float, default=0.10)
    parser.add_argument("--max-gripper-step", type=float, default=0.30)
    parser.add_argument("--infer-delay", type=float, default=0.0)
    parser.add_argument("--save-dir", default="")
    args = parser.parse_args()
    if args.source == "file" and not args.actions:
        parser.error("file 模式需要 --actions")
    safety = SafetyConfig(
        max_joint_step_rad=args.max_joint_step,
        max_gripper_step=args.max_gripper_step,
    )
    state = build_state(
        args.source,
        args.actions,
        args.gripper,
        safety,
        infer_delay=args.infer_delay,
        save_dir=args.save_dir,
    )
    httpd = serve(state, args.host, args.port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[A] 停止", flush=True)
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
