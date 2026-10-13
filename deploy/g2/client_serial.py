"""端口 B：串行阻塞。读机器人，POST 观测，GET Δθ，等规划返回再走下一步。"""

from __future__ import annotations

import argparse

import numpy as np

from deploy.g2.lib.execution import execute_delta, execute_speed
from deploy.g2.lib.joints import make_layout
from deploy.g2.lib.safety import SafetyConfig, SafetyStop
from deploy.g2.lib.speed import SpeedConfig
from deploy.g2.loop import run_serial
from deploy.g2.runtime import add_common_args, close_devices, open_devices, serve_status, RobotStatus

IMPLEMENTED_MODES = ("serial", "serial_speed")


def main() -> None:
    parser = argparse.ArgumentParser(description="端口 B：串行执行归一化 Δθ")
    add_common_args(parser)
    parser.add_argument("--mode", default="serial")
    parser.add_argument("--step-duration", type=float, default=0.5)
    parser.add_argument("--max-joint-vel", type=float, default=0.20)
    parser.add_argument("--max-gripper-vel", type=float, default=0.40)
    args = parser.parse_args()
    if args.mode not in IMPLEMENTED_MODES:
        known = ", ".join(IMPLEMENTED_MODES)
        raise SystemExit(f"模式 {args.mode} 还没有实现。当前可用: {known}。异步用 client_async")

    layout = make_layout(args.gripper)
    safety = SafetyConfig(
        max_joint_step_rad=args.max_joint_step,
        max_gripper_step=args.max_gripper_step,
        limit_margin_rad=args.limit_margin,
        joint_velocity=args.joint_velocity,
    )
    speed = None
    execute = execute_delta
    if args.mode == "serial_speed":
        speed = SpeedConfig(
            step_duration=args.step_duration,
            max_joint_vel=args.max_joint_vel,
            max_gripper_vel=args.max_gripper_vel,
        )

        def execute(robot, action, layout, safety, status_robot=None):
            return execute_speed(
                robot, action, layout, safety, speed, status_robot=status_robot
            )

    status = RobotStatus()
    httpd = serve_status(status, args.host, args.port)
    hardware = None
    cameras = None
    robot = None
    try:
        hardware, robot, status_robot, cameras, kind = open_devices(args, layout)
        speed_text = ""
        if speed is not None:
            speed_text = (
                f"  duration={speed.step_duration:.2f}s"
                f"  max_vel={speed.max_joint_vel:.3f} rad/s"
            )
        print(
            f"[B] {kind}  control={args.mode}  model={args.model_url}  "
            f"horizon={args.open_loop_horizon}  max_step={safety.max_joint_step_rad:.3f} rad"
            f"{speed_text}",
            flush=True,
        )
        status.update(status="running", mode=kind, model_url=args.model_url)

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
            execute=execute,
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
        close_devices(cameras, hardware, robot)
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
