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
            default_value=EnvironmentVariable(
                "ROBOT_ID",
                default_value="robot"
            ),
            description="Name for launch and config resources"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_xacro",
            default_value=EnvironmentVariable(
                "ROBOT_BASE_XACRO",
                default_value="nano_atom_std.urdf.xacro"
            ),
            description="URDF of the robot"
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
            "headless_sim",
            default_value=EnvironmentVariable(
                "ROBOT_BASE_SIM_HEADLESS",
                default_value="false"
            ),
            description="Run simulation without graphical interface"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "world_sim",
            default_value=EnvironmentVariable(
                "ROBOT_BASE_SIM_WORLD",
                default_value="nano_atom_office.world"
            ),
            description="World for simulation"
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

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_rviz",
            default_value=EnvironmentVariable(
                "ROBOT_BASE_RUN_RVIZ",
                default_value="false"
            ),
            description="Run Rviz gui"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_file",
            default_value=EnvironmentVariable(
                "ROBOT_BASE_RVIZ_FILE",
                default_value="base.rviz"
            ),
            description="Set rviz config visualization"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "driver_uri",
            default_value="/dev/ttyAMA_NANO_ATOM",
            description="Nano atom driver phisical address"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "pad_model",
            default_value="terios",
            description="Set gamepad model"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "pad_uri",
            default_value="/dev/input/js_robot",
            description="Set pad physical address"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    robot_xacro = LaunchConfiguration("robot_xacro")
    use_sim = LaunchConfiguration("use_sim")
    headless_sim = LaunchConfiguration("headless_sim")
    world_sim = LaunchConfiguration("world_sim")
    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_a = LaunchConfiguration("initial_pose_a") 
    run_rviz = LaunchConfiguration("run_rviz")
    rviz_file = LaunchConfiguration("rviz_file")
    driver_uri = LaunchConfiguration("driver_uri")
    pad_model = LaunchConfiguration("pad_model")
    pad_uri = LaunchConfiguration("pad_uri")

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
            'hardware_path': hardware_path,
            'driver_uri': driver_uri
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

    teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_teleop'), 'launch/teleop.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'pad_model': pad_model,
            'pad_uri': pad_uri
        }.items()
    )

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_gz_sim'), 'launch/simulation.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'headless_sim': headless_sim,
            'world_sim': world_sim,
            'initial_pose_x': initial_pose_x,
            'initial_pose_y': initial_pose_y,
            'initial_pose_a': initial_pose_a,
        }.items(),
        condition=IfCondition(use_sim)
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_base'), 'launch/rviz.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'rviz_file': rviz_file,
        }.items(),
        condition=IfCondition(run_rviz)
    )

    group = GroupAction([
        PushRosNamespace(LaunchConfiguration('robot_id')),
        description,
        control,
        teleop,
        simulation,
        rviz
    ])

    return LaunchDescription(declared_arguments + [group])