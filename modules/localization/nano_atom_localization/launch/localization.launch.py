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
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import PushRosNamespace
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import GroupAction, DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_id",
            default_value="robot",
            description="Name for launch and config resources"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim",
            default_value="true",
            description="Enable simulation"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_mapping",
            default_value="false",
            description="Enable mapping"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    use_sim = LaunchConfiguration("use_sim")
    run_mapping = LaunchConfiguration("run_mapping")

    localization_2d = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_localization'), 'launch/localization_2d.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'use_sim': use_sim,
        }.items(),
        condition=UnlessCondition(run_mapping)
    )

    mapping_2d = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_localization'), 'launch/mapping_2d.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'use_sim': use_sim,
        }.items(),
        condition=IfCondition(run_mapping)
    )

    group = GroupAction([
        PushRosNamespace(LaunchConfiguration('robot_id')),
        localization_2d,
        mapping_2d
    ])

    return LaunchDescription(declared_arguments + [group])