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

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.conditions import UnlessCondition

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    headless_sim = LaunchConfiguration("headless_sim")
    world_sim = LaunchConfiguration("world_sim")

    world_path = PathJoinSubstitution([
        FindPackageShare('nano_atom_gz_sim'),
        'worlds',
        world_sim
    ])

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': ['-r ', '-s ',  world_path],
            'on_exit_shutdown': 'true'
        }.items(),
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'), 'launch/gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': ['-g'],
            'on_exit_shutdown': 'true'
        }.items(),
        condition=UnlessCondition(headless_sim)
    )

    group = GroupAction([
        gazebo_server,
        gazebo_client,
    ])

    return LaunchDescription([group])