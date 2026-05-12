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

from launch import LaunchDescription
from launch.actions import GroupAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    use_sim = LaunchConfiguration("use_sim")
    pad_model = LaunchConfiguration("pad_model")
    pad_uri = LaunchConfiguration("pad_uri")
    
    pad_twist_params = PathJoinSubstitution([
        FindPackageShare("nano_atom_teleop"),
        "config/gamepad/pad_twist.yaml"
    ])

    pad_map_params = PathJoinSubstitution([
        FindPackageShare("nano_atom_teleop"),
        "config/gamepad",
        PythonExpression(["'", pad_model, ".yaml'"])
    ])

    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joy",
        output="screen",
        respawn=True,
        parameters=[
            {
                'use_sim_time': use_sim,
                'dev': pad_uri
            }
        ]
    )

    roboticarts_pad_node = Node(
        package="roboticarts_pad",
        executable="roboticarts_pad_node",
        name="roboticarts_pad",
        output="screen",
        parameters=[
            pad_twist_params,
            pad_map_params,
            {
                'use_sim_time': use_sim,
                'cmd_vel_topic': 'pad_teleop/cmd_vel',
                # TODO(robert): Driver must be agnostic for pad node
                'pad_settings.driver': 'generic',
                'pad_settings.use_stamped_vel': True
            }
        ]
    )

    group = GroupAction([
        joy_node,
        roboticarts_pad_node,
    ])

    return LaunchDescription([group])