"""串行客户端和异步客户端共用的参数、状态端口和机器人打开方式。"""

from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from deploy.g2.lib.camera import GdkCameras, MockCameras
from deploy.g2.lib.robot import GdkRobot, MockRobot


class RobotStatus:
    def __init__(self):
        self.lock = threading.Lock()
        self.payload = {"role": "robot", "status": "starting", "steps": 0}

    def update(self, **fields) -> None:
        with self.lock:
            self.payload.update(fields)

    def snapshot(self) -> dict:
        with self.lock:
            return dict(self.payload)


def serve_status(status: RobotStatus, host: str, port: int) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self):  # noqa: N802
            path = self.path.split("?", 1)[0]
            if path not in {"/health", "/status"}:
                body = {"error": "not found"}
                code = 404
            else:
                body = status.snapshot()
                code = 200
            data = json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, fmt: str, *args) -> None:
            return

    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer((host, port), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bound = httpd.server_address
    print(f"[B] 机器人端口 http://{bound[0]}:{bound[1]}", flush=True)
    return httpd


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model-url", default="http://127.0.0.1:8800")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8801)
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--no-move", action="store_true", help="读真机状态并计算指令，但不下发")
    parser.add_argument("--no-camera", action="store_true", help="用空白图像，只打通关节接口")
    parser.add_argument("--task", default="agibot dual arm")
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--open-loop-horizon", type=int, default=1)
    parser.add_argument("--gripper", default="omnipicker", choices=["omnipicker", "dahuan", "ctek90d"])
    parser.add_argument("--max-joint-step", type=float, default=0.10)
    parser.add_argument("--max-gripper-step", type=float, default=0.30)
    parser.add_argument("--limit-margin", type=float, default=0.02)
    parser.add_argument("--joint-velocity", type=float, default=0.20)
    parser.add_argument("--image-height", type=int, default=224)
    parser.add_argument("--image-width", type=int, default=224)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--verbose", action="store_true", default=True)


def open_devices(args, layout):
    hardware = None
    if args.mock or args.no_move:
        if args.no_move and not args.mock:
            hardware = GdkRobot(layout)
            robot = MockRobot(layout, q=hardware.read_radians())
            status_robot = hardware
        else:
            robot = MockRobot(layout)
            status_robot = None
    else:
        robot = GdkRobot(layout)
        status_robot = None

    if args.mock or args.no_camera:
        cameras = MockCameras(args.image_height, args.image_width)
    else:
        cameras = GdkCameras()
    kind = "mock" if args.mock else ("no-move" if args.no_move else "gdk")
    return hardware, robot, status_robot, cameras, kind


def close_devices(cameras, hardware, robot) -> None:
    if cameras is not None:
        cameras.close()
    if hardware is not None:
        hardware.close()
    elif robot is not None:
        robot.close()
