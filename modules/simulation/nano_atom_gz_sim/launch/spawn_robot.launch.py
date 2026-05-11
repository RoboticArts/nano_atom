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

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import GroupAction
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    robot_name = LaunchConfiguration("robot_name", default="nano_atom")
    initial_pose_x = LaunchConfiguration("initial_pose_x", default="0.0")
    initial_pose_y = LaunchConfiguration("initial_pose_y", default="0.0")
    initial_pose_a = LaunchConfiguration("initial_pose_a", default="0.0")            

    gazebo_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', [robot_id, '/', robot_name], # Robot name for Gazebo world
            '-topic', "robot_description",
            '-x', initial_pose_x,
            '-y', initial_pose_y,
            '-z', "0.0",
            '-Y', initial_pose_a,
        ],
        output='screen',
    )

    bridge_config = PathJoinSubstitution([
        FindPackageShare('nano_atom_gz_sim'),
        'config/bridge.yaml'
    ])

    gazebo_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {'config_file': bridge_config},
        ],
    )

    group = GroupAction([
        gazebo_spawn,
        gazebo_bridge
    ])

    return LaunchDescription([group])