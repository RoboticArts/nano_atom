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
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import PushRosNamespace
from launch.actions import GroupAction
from launch.conditions import IfCondition

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
            "robot_xacro",
            default_value="nano_atom_std.urdf.xacro",
            description="URDF of the robot"
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
            "initial_pose_x",
            default_value="0.0",
            description="Set the robot pose on the X axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_y",
            default_value="0.0",
            description="Set the robot pose on the Y axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_a",
            default_value="0.0",
            description="Set the robot orientation in yaw"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_rviz",
            default_value="false",
            description="Run Rviz gui"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    robot_xacro = LaunchConfiguration("robot_xacro")
    use_sim = LaunchConfiguration("use_sim")
    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_a = LaunchConfiguration("initial_pose_a") 
    run_rviz = LaunchConfiguration("run_rviz")

    robot_prefix = PythonExpression(["'", robot_id, "/'"])

    # Set the controllers configuration for ros2_controller
    # use_sim = false -> Controller package  -> node -> Load config in controller_manager
    # use_sim = true  -> Description package -> urdf -> Load config in gz_ros2_control
    controller_path = PathJoinSubstitution([
        FindPackageShare('nano_atom_control'),
        'config/diff_controller.yaml'
    ])

    # Set the parameters for hardware interface
    # use_sim = false -> Description package -> urdf -> Load config in ros2_control
    # use_sim = true  -> Description package -> urdf -> Not use config
    hardware_path = PathJoinSubstitution([
        FindPackageShare('nano_atom_hardware'),
        'config/hardware.yaml'
    ])

    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_description'), 'launch/description.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'robot_xacro': robot_xacro,
            'controller_sim_path': controller_path, # Used for simulation
            'hardware_path': hardware_path
        }.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_control'), 'launch/control.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'controller_path': controller_path, # Used for real robot
        }.items()
    )

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_simulation'), 'launch/simulation.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'initial_pose_x': initial_pose_x,
            'initial_pose_y': initial_pose_y,
            'initial_pose_a': initial_pose_a,
        }.items(),
        condition=IfCondition(use_sim)
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_description'), 'launch/rviz.launch.py'
            ])
        ),
        condition=IfCondition(run_rviz)
    )

    group = GroupAction([
        PushRosNamespace(LaunchConfiguration('robot_id')),
        description,
        control,
        simulation,
        rviz
    ])

    return LaunchDescription(declared_arguments + [group])