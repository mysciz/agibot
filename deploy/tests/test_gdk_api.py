"""用假的 agibot_gdk 核对阻塞控制接口的调用方式，不连接机器人。"""

from __future__ import annotations

import os
import sys
import unittest

import numpy as np

from deploy.g2.lib import gdk_session
from deploy.g2.lib.joints import ARM_NAMES, make_layout
from deploy.g2.lib.robot import GdkRobot


class _FakeRobot:
    instances = []

    def __init__(self):
        self.arm_calls = []
        self.ee_calls = []
        self.servo_calls = []
        _FakeRobot.instances.append(self)

    def get_joint_states(self):
        # position 故意填成别的值，读取必须用 motor_position。
        return {
            "nums": len(ARM_NAMES),
            "states": [
                {"name": name, "motor_position": 0.1, "position": 9.0}
                for name in ARM_NAMES
            ],
        }

    def get_end_state(self):
        return {
            "left_end_state": {"names": ["left"], "end_states": [{"position": -0.2}]},
            "right_end_state": {"names": ["right"], "end_states": [{"position": -0.3}]},
        }

    def get_whole_body_status(self):
        return {
            "left_arm_error": 0,
            "right_arm_error": 0,
            "left_end_error": 0,
            "right_end_error": 0,
            "left_arm_estop": False,
            "right_arm_estop": False,
        }

    def move_arm_joint(self, positions, velocities, group):
        self.arm_calls.append((list(positions), list(velocities), group))

    def move_ee_pos(self, joint_states):
        self.ee_calls.append(joint_states)

    def joint_servo_control(self, request, enable_low_latency=False):
        self.servo_calls.append((request, enable_low_latency))


class _FakeGDK:
    class GDKRes:
        kSuccess = 0

    class JointState:
        def __init__(self):
            self.position = None

    class JointServoControlReq:
        def __init__(self):
            self.control_period = None
            self.joint_names = None
            self.joint_positions = None
            self.joint_velocities = None

    class JointStates:
        def __init__(self):
            self.group = None
            self.target_type = None
            self.states = None
            self.nums = None

    Robot = _FakeRobot

    def gdk_init(self):
        return _FakeGDK.GDKRes.kSuccess

    def gdk_release(self):
        self.released = True
        return _FakeGDK.GDKRes.kSuccess


class GdkApiTest(unittest.TestCase):
    def setUp(self):
        self._previous = sys.modules.get("agibot_gdk")
        self._ready = gdk_session._ready
        self._locator = os.environ.get("LOCATOR_IP")
        self._uri = os.environ.get("AORTA_DISCOVERY_URI")
        _FakeRobot.instances = []
        self.fake = _FakeGDK()
        sys.modules["agibot_gdk"] = self.fake
        gdk_session._ready = False

    def tearDown(self):
        gdk_session._ready = self._ready
        if self._previous is None:
            sys.modules.pop("agibot_gdk", None)
        else:
            sys.modules["agibot_gdk"] = self._previous
        self._restore("LOCATOR_IP", self._locator)
        self._restore("AORTA_DISCOVERY_URI", self._uri)

    @staticmethod
    def _restore(key, value):
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    def test_missing_discovery_does_not_init(self):
        os.environ.pop("LOCATOR_IP", None)
        os.environ.pop("AORTA_DISCOVERY_URI", None)
        with self.assertRaises(RuntimeError):
            gdk_session.ensure_gdk()
        self.assertFalse(gdk_session._ready)

    def test_blocking_arm_and_gripper_calls(self):
        os.environ["LOCATOR_IP"] = "10.42.1.102"
        robot = GdkRobot(make_layout("omnipicker"), init_sleep_s=0)
        radians = robot.read_radians()
        self.assertTrue(np.allclose(radians[:14], 0.1))
        self.assertAlmostEqual(radians[14], -0.2)
        self.assertAlmostEqual(radians[15], -0.3)

        robot.move_arms(np.zeros(14), 0.2)
        robot.move_grippers(np.array([-0.1, -0.4]))
        fake_robot = _FakeRobot.instances[0]
        positions, velocities, group = fake_robot.arm_calls[0]
        self.assertEqual(group, 2)
        self.assertEqual(len(positions), 14)
        self.assertEqual(velocities, [0.2] * 14)

        command = fake_robot.ee_calls[0]
        self.assertEqual(command.group, "dual_tool")
        self.assertEqual(command.target_type, "omnipicker")
        self.assertEqual(command.nums, 2)
        self.assertAlmostEqual(command.states[0].position, -0.1)
        self.assertAlmostEqual(command.states[1].position, -0.4)
        self.assertFalse(robot.read_status()["right_arm_estop"])

        target = np.linspace(-0.2, 0.2, 16)
        robot.servo_joints(target, 0.012)
        request, low_latency = fake_robot.servo_calls[0]
        self.assertFalse(low_latency)
        self.assertAlmostEqual(request.control_period, 0.012)
        self.assertEqual(len(request.joint_names), 16)
        self.assertEqual(request.joint_names[0], "idx21_arm_l_joint1")
        self.assertEqual(request.joint_names[14], "idx31_gripper_l_inner_joint1")
        self.assertEqual(len(request.joint_positions), 16)
        self.assertEqual(request.joint_velocities, [])
        self.assertAlmostEqual(request.joint_positions[0], target[0])

        robot.close()
        self.assertTrue(self.fake.released)
        self.assertFalse(gdk_session._ready)


if __name__ == "__main__":
    unittest.main()
