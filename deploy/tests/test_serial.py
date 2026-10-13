"""归一化 Δθ、文件动作源，以及端口 A/B 的串行闭环。不连接机器人。"""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path

import numpy as np

from deploy.g2.lib.action_source import FileSource, load_steps, parse_command
from deploy.g2.lib.actions import decode_normalized_delta, delta_scales, encode_delta_rad
from deploy.g2.lib.camera import prepare_image
from deploy.g2.lib.execution import execute_delta, execute_speed
from deploy.g2.lib.speed import SpeedConfig, angles_to_velocities
from deploy.g2.lib.joints import make_layout, normalize
from deploy.g2.lib.model_client import post_observation
from deploy.g2.lib.robot import MockRobot
from deploy.g2.lib.safety import SafetyConfig, SafetyStop
from deploy.g2.loop import run_serial
from deploy.g2.server import build_state, serve


class DeltaTest(unittest.TestCase):
    def setUp(self):
        self.safety = SafetyConfig(max_joint_step_rad=0.10, max_gripper_step=0.30)
        self.scales = delta_scales(self.safety)

    def test_half_is_zero_and_ends_are_scale(self):
        zero = decode_normalized_delta(np.full(16, 0.5), self.scales)
        self.assertTrue(np.allclose(zero, 0.0))
        positive = decode_normalized_delta(np.ones(16), self.scales)
        self.assertAlmostEqual(positive[0], 0.10)
        self.assertAlmostEqual(positive[14], 0.30)
        negative = decode_normalized_delta(np.zeros(16), self.scales)
        self.assertAlmostEqual(negative[0], -0.10)

    def test_radian_file_roundtrip(self):
        delta = np.zeros(16)
        delta[0] = 0.05
        encoded = encode_delta_rad(delta, self.scales)
        self.assertAlmostEqual(encoded[0], 0.75)
        self.assertAlmostEqual(encoded[1], 0.5)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "steps.json"
            path.write_text(json.dumps({"unit": "rad", "steps": [delta.tolist()]}), encoding="utf-8")
            loaded = load_steps(path, self.scales)
        self.assertTrue(np.allclose(loaded[0], encoded))

    def test_terminal_lines(self):
        hold = parse_command("hold", self.scales)
        self.assertTrue(np.allclose(hold, 0.5))
        self.assertIsNone(parse_command("quit", self.scales))
        jog = parse_command("rad " + " ".join(["0.05"] + ["0"] * 15), self.scales)
        self.assertAlmostEqual(jog[0], 0.75)


class ExecuteTest(unittest.TestCase):
    def test_hold_does_not_move(self):
        layout = make_layout()
        robot = MockRobot(layout)
        safety = SafetyConfig()
        execute_delta(robot, np.full(16, 0.5), layout, safety)
        self.assertEqual(robot.arm_commands, [])
        self.assertEqual(robot.gripper_commands, [])

    def test_estop_blocks(self):
        layout = make_layout()
        robot = MockRobot(layout)
        robot.status["right_arm_estop"] = True
        with self.assertRaises(SafetyStop):
            execute_delta(robot, np.ones(16), layout, SafetyConfig())
        self.assertEqual(robot.arm_commands, [])

    def test_positive_delta_is_applied_from_current_pose(self):
        layout = make_layout()
        robot = MockRobot(layout)
        start = robot.read_radians()[0]
        safety = SafetyConfig(max_joint_step_rad=0.10, max_gripper_step=0.30)
        action = np.full(16, 0.5)
        action[0] = encode_delta_rad(_one_joint(0.05), delta_scales(safety))[0]
        execute_delta(robot, action, layout, safety)
        self.assertAlmostEqual(robot.read_radians()[0], start + 0.05, places=6)


class SpeedModeTest(unittest.TestCase):
    def test_large_angle_becomes_capped_velocity(self):
        delta = _one_joint(0.10)
        config = SpeedConfig(step_duration=0.5, max_joint_vel=0.10, max_gripper_vel=0.40)
        velocity, step = angles_to_velocities(delta, config)
        self.assertAlmostEqual(velocity[0], 0.10)
        self.assertAlmostEqual(step[0], 0.05)

    def test_execute_speed_sends_per_joint_velocity(self):
        layout = make_layout()
        robot = MockRobot(layout)
        start = robot.read_radians()[0]
        safety = SafetyConfig(max_joint_step_rad=0.20, max_gripper_step=0.30)
        speed = SpeedConfig(step_duration=0.5, max_joint_vel=0.20, max_gripper_vel=0.40)
        action = np.full(16, 0.5)
        action[0] = encode_delta_rad(_one_joint(0.05), delta_scales(safety))[0]
        record = execute_speed(robot, action, layout, safety, speed)
        self.assertAlmostEqual(record.velocity[0], 0.10, places=5)
        self.assertAlmostEqual(robot.read_radians()[0], start + 0.05, places=5)
        self.assertAlmostEqual(robot.arm_velocities[0][0], 0.10, places=5)


class SerialProtocolTest(unittest.TestCase):
    def test_post_obs_then_get_delta_chunk(self):
        safety = SafetyConfig(max_joint_step_rad=0.10, max_gripper_step=0.30, limit_margin_rad=0.02)
        state = build_state(
            "file",
            str(Path(__file__).resolve().parents[1] / "examples" / "joint0_wiggle.json"),
            "omnipicker",
            safety,
        )
        httpd = serve(state, "127.0.0.1", 0)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            port = httpd.server_address[1]
            layout = make_layout()
            robot = MockRobot(layout)
            start = robot.read_radians().copy()
            records = run_serial(
                robot,
                _TinyCameras(),
                f"http://127.0.0.1:{port}",
                layout,
                safety,
                max_steps=4,
                open_loop_horizon=2,
                image_height=8,
                image_width=8,
                verbose=False,
            )
        finally:
            httpd.shutdown()
            httpd.server_close()

        self.assertEqual(len(records), 4)
        self.assertEqual(state.observations, 2)
        self.assertAlmostEqual(records[0].delta_rad[0], 0.05, places=6)
        self.assertAlmostEqual(records[2].delta_rad[0], -0.05, places=6)
        self.assertTrue(np.allclose(robot.read_radians(), start, atol=1e-6))
        self.assertEqual(prepare_image(np.zeros((2, 2, 3), np.uint8), 8, 8).shape, (8, 8, 3))


class SaveObservationTest(unittest.TestCase):
    def test_posted_cameras_are_written(self):
        safety = SafetyConfig(max_joint_step_rad=0.10, max_gripper_step=0.30)
        with tempfile.TemporaryDirectory() as folder:
            state = build_state(
                "file",
                str(Path(__file__).resolve().parents[1] / "examples" / "joint0_wiggle.json"),
                "omnipicker",
                safety,
                save_dir=folder,
            )
            httpd = serve(state, "127.0.0.1", 0)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                port = httpd.server_address[1]
                cameras = _TinyCameras()
                frames = {name: prepare_image(image, 8, 8) for name, image in cameras.read().items()}
                proprio = np.zeros(16)
                post_observation(
                    f"http://127.0.0.1:{port}",
                    frames,
                    normalize(proprio, make_layout().limits),
                    proprio,
                    "test",
                )
            finally:
                httpd.shutdown()
                httpd.server_close()

            saved = Path(folder) / "0001"
            self.assertTrue((saved / "head.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
            self.assertTrue((saved / "left_wrist.png").is_file())
            self.assertTrue((saved / "right_wrist.png").is_file())
            stored = json.loads((saved / "proprio.json").read_text(encoding="utf-8"))
            self.assertEqual(len(stored["proprio_rad"]), 16)


def _one_joint(value: float) -> np.ndarray:
    delta = np.zeros(16)
    delta[0] = value
    return delta


class _TinyCameras:
    def read(self):
        return {
            "head": np.full((8, 8, 3), 20, dtype=np.uint8),
            "left_wrist": np.full((8, 8, 3), 80, dtype=np.uint8),
            "right_wrist": np.full((8, 8, 3), 160, dtype=np.uint8),
        }

    def close(self):
        return None


if __name__ == "__main__":
    unittest.main()
