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
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import GroupAction

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    robot_name = LaunchConfiguration("robot_name", default="nano_atom")
    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_a = LaunchConfiguration("initial_pose_a")            

    spawn_gazebo_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_gz_sim'), 'launch/spawn_world.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
        }.items(),
    )

    spawn_gazebo_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_gz_sim'), 'launch/spawn_robot.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'robot_name': robot_name,
            'initial_pose_x': initial_pose_x,
            'initial_pose_y': initial_pose_y,
            'initial_pose_a': initial_pose_a,
        }.items(),
    )

    group = GroupAction([
        spawn_gazebo_world,
        spawn_gazebo_robot
    ])

    return LaunchDescription([group])