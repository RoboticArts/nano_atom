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

from launch.actions import RegisterEventHandler, GroupAction, LogInfo
from launch_ros.actions import Node, PushRosNamespace
from launch import LaunchDescription
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    use_sim = LaunchConfiguration("use_sim")
    controller_path = LaunchConfiguration("controller_path")

    # Run controller_manager:
    #  - Register controllers
    #  - Load hardware configuration
    # use_sim = false -> Run controller manager here
    # use_sim = true -> Not run controller manager here because Gazebo creates it 
    ros2_control = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controller_path],
        output="both",
        condition=UnlessCondition(use_sim)
    )

    # Run joint_state_broadcaster controller
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
        ],
    )

    # Run robot_base_controller controller
    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "robot_base_controller",
        ]
    )

    robot_controller_spawner_after_joint_state = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[
                GroupAction([
                    # We need to redeclare PushRosNamespace here because event handlers (like OnProcessExit)
                    # do not automatically inherit the namespace from the parent launch scope
                    PushRosNamespace(robot_id), 
                    LogInfo(msg='joint_state_broadcaster spawned, spawning robot_controller'),
                    robot_controller_spawner
                ])
            ],
        )
    )

    group = GroupAction([
        ros2_control,
        joint_state_broadcaster_spawner,
        robot_controller_spawner_after_joint_state
    ])

    return LaunchDescription([group])