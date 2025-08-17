# Copyright (C) 2025, Robotic Arts
#
# This file is part of nano_atom.
#
# nano_atom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nano_atom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with nano_atom.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Robert Vasquez Zavaleta


from launch_ros.actions import Node
from launch import LaunchDescription
from launch_ros.descriptions import ParameterValue
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch.actions import GroupAction
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    use_sim = LaunchConfiguration("use_sim")
    robot_xacro = LaunchConfiguration("robot_xacro")
    controller_sim_path = LaunchConfiguration("controller_sim_path")
    hardware_path = LaunchConfiguration("hardware_path")

    robot_xacro_path = PathJoinSubstitution([
        FindPackageShare('nano_atom_description'),
        'robots',
        robot_xacro
    ])

    robot_description_content = Command(
        [
            FindExecutable(name='xacro'),
            ' ',
            robot_xacro_path,
            ' ',
            'robot_id:=', robot_id,
            ' ',
            'prefix:=', robot_prefix,
            ' ',
            'use_sim:=', use_sim,
            ' ',
            'controller_sim_path:=', controller_sim_path,
            ' ',
            'hardware_path:=', hardware_path,
        ]
    )

    robot_description = ParameterValue(robot_description_content, value_type=str)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[
            {
              'robot_description': robot_description,
              'publish_frequency': 100.0,
              'use_sim_time': use_sim
            }
        ],
    )

    group = GroupAction([
        robot_state_publisher
    ])

    return LaunchDescription([group])