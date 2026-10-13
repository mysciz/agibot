"""端口 B：异步播放。100Hz 伺服继续走，下一块在缓冲区快空时去要。"""

from __future__ import annotations

import argparse

from deploy.g2.async_loop import run_async
from deploy.g2.lib.joints import make_layout
from deploy.g2.lib.safety import SafetyConfig, SafetyStop
from deploy.g2.lib.speed import SpeedConfig
from deploy.g2.runtime import add_common_args, close_devices, open_devices, serve_status, RobotStatus


def main() -> None:
    parser = argparse.ArgumentParser(description="端口 B：异步播放归一化 Δθ")
    add_common_args(parser)
    parser.add_argument("--step-duration", type=float, default=0.5)
    parser.add_argument("--max-joint-vel", type=float, default=0.20)
    parser.add_argument("--max-gripper-vel", type=float, default=0.40)
    parser.add_argument("--infer-delay", type=float, default=0.0)
    parser.add_argument("--prefetch-margin", type=float, default=0.05)
    parser.add_argument("--servo-hz", type=float, default=100.0)
    parser.add_argument("--control-period", type=float, default=0.0)
    args = parser.parse_args()

    layout = make_layout(args.gripper)
    safety = SafetyConfig(
        max_joint_step_rad=args.max_joint_step,
        max_gripper_step=args.max_gripper_step,
        limit_margin_rad=args.limit_margin,
        joint_velocity=args.joint_velocity,
    )
    speed = SpeedConfig(
        step_duration=args.step_duration,
        max_joint_vel=args.max_joint_vel,
        max_gripper_vel=args.max_gripper_vel,
    )
    status = RobotStatus()
    httpd = serve_status(status, args.host, args.port)
    hardware = None
    cameras = None
    robot = None
    try:
        hardware, robot, status_robot, cameras, kind = open_devices(args, layout)
        print(
            f"[B] {kind}  control=async  model={args.model_url}  "
            f"horizon={args.open_loop_horizon}  max_step={safety.max_joint_step_rad:.3f} rad"
            f"  duration={speed.step_duration:.2f}s"
            f"  infer={args.infer_delay:.2f}s"
            f"  servo={args.servo_hz:.0f}Hz",
            flush=True,
        )
        status.update(status="running", mode=kind, model_url=args.model_url)

        def _on_chunk(steps, _samples):
            status.update(steps=steps)

        result = run_async(
            robot,
            cameras,
            args.model_url,
            layout,
            safety,
            speed,
            task=args.task,
            max_steps=args.max_steps,
            open_loop_horizon=args.open_loop_horizon,
            infer_delay=args.infer_delay,
            prefetch_margin=args.prefetch_margin,
            servo_hz=args.servo_hz,
            control_period=args.control_period,
            image_height=args.image_height,
            image_width=args.image_width,
            timeout=args.timeout,
            verbose=args.verbose,
            status_robot=status_robot,
            on_chunk=_on_chunk,
        )
        status.update(status="done", steps=result.steps)
        print(
            f"[B] 完成 {result.steps} 步  servo={result.sent}  hold={result.holds}",
            flush=True,
        )
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
