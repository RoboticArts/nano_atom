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
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution, PythonExpression
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
            default_value=EnvironmentVariable(
                "ROBOT_ID",
                default_value="robot"
            ),
            description="Name for launch and config resources"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim",
            default_value=EnvironmentVariable(
                "ROBOT_USE_SIM",
                default_value="true"
            ),
            description="Enable simulation"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_mapping",
            default_value=EnvironmentVariable(
                "ROBOT_LOCALIZATION_RUN_MAPPING",
                default_value="false"
            ),
            description="Enable mapping"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "map_name",
            default_value=EnvironmentVariable(
                "ROBOT_LOCALIZATION_MAP_NAME",
                default_value="false"
            ),
            description="Map name for localization"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "laser_topic",
            default_value=EnvironmentVariable(
                "ROBOT_LOCALIZATION_LASER_TOPIC",
                default_value="scan"
            ),
            description="Laser topic for localization and mapping"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_x",
            default_value=EnvironmentVariable(
                "ROBOT_INITIAL_POSE_X",
                default_value="0.0"
            ),
            description="Set the robot pose on the X axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_y",
            default_value=EnvironmentVariable(
                "ROBOT_INITIAL_POSE_Y",
                default_value="0.0"
            ),
            description="Set the robot pose on the Y axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_a",
            default_value=EnvironmentVariable(
                "ROBOT_INITIAL_POSE_A",
                default_value="0.0"
            ),
            description="Set the robot orientation in yaw"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    use_sim = LaunchConfiguration("use_sim")
    run_mapping = LaunchConfiguration("run_mapping")
    map_name = LaunchConfiguration("map_name")
    laser_topic = LaunchConfiguration("laser_topic")
    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_a = LaunchConfiguration("initial_pose_a")
    
    robot_prefix = PythonExpression(["'", robot_id, "/'"])

    localization_2d = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_localization'), 'launch/localization_2d.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'map_name': map_name,
            'laser_topic': laser_topic,
            'initial_pose_x': initial_pose_x,
            'initial_pose_y': initial_pose_y,
            'initial_pose_a': initial_pose_a
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
            'robot_prefix': robot_prefix,
            'laser_topic': laser_topic,
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