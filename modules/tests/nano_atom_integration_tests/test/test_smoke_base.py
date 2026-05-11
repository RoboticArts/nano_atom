# Copyright (C) 2025, Robotic Arts
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: Robert Vasquez Zavaleta

import unittest
import pytest
import subprocess

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, EmitEvent
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.events import Shutdown
import launch_testing
from launch_testing.actions import ReadyToTest
from launch.substitutions import PathJoinSubstitution 
from launch_ros.substitutions import FindPackageShare

@pytest.mark.launch_test
def generate_test_description():

    base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_base'), 'launch/base.launch.py'
            ])
        ),
        launch_arguments={
            'run_rviz': 'false',
            'headless_sim': 'true',
        }.items()
    )

    ready_to_test = ReadyToTest()

    shutdown_after_timer = TimerAction(
        period=30.0,
        actions=[EmitEvent(event=Shutdown(reason="Timeout reached"))]
    )

    ld = LaunchDescription([
        base,
        ready_to_test,
        shutdown_after_timer
    ])

    return ld, {}


import unittest
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class TestLaunchAlive(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = rclpy.create_node("test_node")
        cls.msg_received = False

        def callback(msg):
            cls.msg_received = True
            cls.last_msg = msg

        cls.sub = cls.node.create_subscription(
            Odometry,
            "/robot/robot_base_controller/odom",
            callback,
            10
        )

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_odom_topic_active(self):
        timeout_sec = 20.0  # Wait until 20 seconds
        start = self.node.get_clock().now()

        while (self.node.get_clock().now() - start).nanoseconds < timeout_sec * 1e9:
            rclpy.spin_once(self.node, timeout_sec=0.1)
            if self.msg_received:
                break

        self.assertTrue(
            self.msg_received,
            "No messages for /robot/robot_base_controller/odom"
        )


@launch_testing.post_shutdown_test()
class TestAfterShutdown(unittest.TestCase):

    # Kill gz sim because it always becomes a zombie
    def test_kill_leftover_gz(self, proc_info):
        subprocess.run(["pkill", "-9", "-f", "gz sim"], check=False)

    def test_no_unexpected_errors(self, proc_info):
        launch_testing.asserts.assertExitCodes(
            proc_info,
            allowable_exit_codes=[0, -15, -9, -2]
        )