"""端口 B：机器人控制侧。

从机器人读状态，POST 到端口 A，再 GET 归一化 Δθ 动作块，串行阻塞执行。
本进程同时在 ROBOT_PORT 上提供 /health 和 /status。
"""

from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np

from deploy.g2.lib.camera import GdkCameras, MockCameras
from deploy.g2.lib.joints import make_layout
from deploy.g2.lib.robot import GdkRobot, MockRobot
from deploy.g2.lib.safety import SafetyConfig, SafetyStop
from deploy.g2.loop import run_serial


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


def _serve_status(status: RobotStatus, host: str, port: int) -> ThreadingHTTPServer:
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


def main() -> None:
    parser = argparse.ArgumentParser(description="端口 B：串行执行归一化 Δθ")
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
    args = parser.parse_args()

    layout = make_layout(args.gripper)
    safety = SafetyConfig(
        max_joint_step_rad=args.max_joint_step,
        max_gripper_step=args.max_gripper_step,
        limit_margin_rad=args.limit_margin,
        joint_velocity=args.joint_velocity,
    )
    status = RobotStatus()
    httpd = _serve_status(status, args.host, args.port)
    hardware = None
    cameras = None
    try:
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

        mode = "mock" if args.mock else ("no-move" if args.no_move else "gdk")
        print(
            f"[B] {mode}  model={args.model_url}  "
            f"horizon={args.open_loop_horizon}  max_step={safety.max_joint_step_rad:.3f} rad",
            flush=True,
        )
        status.update(status="running", mode=mode, model_url=args.model_url)

        def _on_step(record, step):
            status.update(
                steps=step,
                last_delta_rad=np.round(record.delta_rad, 5).tolist(),
                last_command_rad=np.round(record.command, 5).tolist(),
            )

        records = run_serial(
            robot,
            cameras,
            args.model_url,
            layout,
            safety,
            task=args.task,
            max_steps=args.max_steps,
            open_loop_horizon=args.open_loop_horizon,
            image_height=args.image_height,
            image_width=args.image_width,
            timeout=args.timeout,
            verbose=args.verbose,
            status_robot=status_robot,
            on_step=_on_step,
        )
        status.update(status="done", steps=len(records))
        print(f"[B] 完成 {len(records)} 步", flush=True)
    except SafetyStop as exc:
        status.update(status="stopped", error=str(exc))
        print(f"[B] 安全停止: {exc}", flush=True)
        raise SystemExit(2) from exc
    except KeyboardInterrupt:
        status.update(status="interrupted")
        print("\n[B] 已中断", flush=True)
    finally:
        if cameras is not None:
            cameras.close()
        if hardware is not None:
            hardware.close()
        elif "robot" in locals():
            robot.close()
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
