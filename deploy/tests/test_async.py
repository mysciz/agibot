"""异步播放：插值、提前取下一块，以及带推理延迟的本地闭环。"""

from __future__ import annotations

import threading
import unittest
from pathlib import Path

import numpy as np

from deploy.g2.async_loop import run_async
from deploy.g2.lib.actions import delta_scales, encode_delta_rad
from deploy.g2.lib.async_traj import plan_chunk, playback_holds, ticks_per_step
from deploy.g2.lib.joints import make_layout
from deploy.g2.lib.robot import MockRobot
from deploy.g2.lib.safety import SafetyConfig
from deploy.g2.lib.speed import SpeedConfig
from deploy.g2.server import build_state, serve
from deploy.tests.test_serial import _TinyCameras, _one_joint


class AsyncPlanTest(unittest.TestCase):
    def test_chunk_is_interpolated_to_the_step_end(self):
        layout = make_layout()
        safety = SafetyConfig(max_joint_step_rad=0.10, max_gripper_step=0.30)
        speed = SpeedConfig(step_duration=0.05, max_joint_vel=2.0, max_gripper_vel=2.0)
        start = np.zeros(16)
        action = np.full(16, 0.5)
        action[0] = encode_delta_rad(_one_joint(0.05), delta_scales(safety))[0]
        samples = plan_chunk(start, action.reshape(1, 16), layout, safety, speed, dt=0.01)
        self.assertEqual(len(samples), ticks_per_step(0.05, 0.01))
        self.assertAlmostEqual(samples[-1, 0], 0.05, places=6)
        self.assertGreater(samples[0, 0], 0.0)
        self.assertLess(samples[0, 0], samples[-1, 0])

    def test_early_prefetch_has_no_midstream_gap(self):
        opening, gaps = playback_holds([50, 50], delay_ticks=10, lead_ticks=12)
        self.assertEqual(opening, 10)
        self.assertEqual(gaps, 0)

    def test_late_chunk_holds_in_the_middle(self):
        _opening, gaps = playback_holds([50, 50], delay_ticks=20, lead_ticks=5)
        self.assertGreater(gaps, 0)


class AsyncLoopTest(unittest.TestCase):
    def test_delayed_file_returns_to_start(self):
        safety = SafetyConfig(max_joint_step_rad=0.10, max_gripper_step=0.30)
        speed = SpeedConfig(step_duration=0.05, max_joint_vel=2.0, max_gripper_vel=2.0)
        state = build_state(
            "file",
            str(Path(__file__).resolve().parents[1] / "examples" / "joint0_wiggle.json"),
            "omnipicker",
            safety,
            infer_delay=0.04,
        )
        httpd = serve(state, "127.0.0.1", 0)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            port = httpd.server_address[1]
            layout = make_layout()
            robot = MockRobot(layout)
            start = robot.read_radians().copy()
            result = run_async(
                robot,
                _TinyCameras(),
                f"http://127.0.0.1:{port}",
                layout,
                safety,
                speed,
                max_steps=4,
                open_loop_horizon=2,
                infer_delay=0.04,
                prefetch_margin=0.0,
                servo_hz=100.0,
                image_height=8,
                image_width=8,
                verbose=False,
            )
        finally:
            httpd.shutdown()
            httpd.server_close()

        self.assertEqual(result.steps, 4)
        self.assertEqual(result.sent, 4 * ticks_per_step(0.05, 0.01))
        self.assertGreater(result.holds, 0)
        self.assertEqual(state.observations, 2)
        peak = max(command[0] - start[0] for command in robot.servo_commands)
        self.assertAlmostEqual(peak, 0.10, places=3)
        self.assertTrue(np.allclose(robot.read_radians(), start, atol=1e-6))
