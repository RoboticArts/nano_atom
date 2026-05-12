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
            "laser_model",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_LASER_MODEL", 
                default_value=""
            ),
            description="Laser model name"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "laser_id",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_LASER_ID", 
                default_value=""
            ),
            description="Laser name"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "laser_uri",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_LASER_URI", 
                default_value=""
            ),
            description="Laser physical address"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "laser_max_angle",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_LASER_MAX_ANGLE", 
                default_value="3.14"
            ),
            description="Max laser angle in radians"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "laser_min_angle",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_LASER_MIN_ANGLE", 
                default_value="-3.14"
            ),
            description="Min laser angle in radians"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "camera_model",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_CAMERA_MODEL", 
                default_value=""
            ),
            description="Camera model name"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "camera_id",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_CAMERA_ID", 
                default_value=""
            ),
            description="Camera name"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "camera_uri",
            default_value=EnvironmentVariable(
                "ROBOT_DEVICES_CAMERA_URI", 
                default_value=""
            ),
            description="Camera physical address"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    use_sim = LaunchConfiguration("use_sim")
    laser_model = LaunchConfiguration("laser_model")
    laser_id = LaunchConfiguration("laser_id")
    laser_uri = LaunchConfiguration("laser_uri")
    laser_max_angle = LaunchConfiguration("laser_max_angle")
    laser_min_angle = LaunchConfiguration("laser_min_angle")
    camera_model = LaunchConfiguration("camera_model")
    camera_id = LaunchConfiguration("camera_id")
    camera_uri = LaunchConfiguration("camera_uri")

    robot_prefix = PythonExpression(["'", robot_id, "/'"])

    laser = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_devices'), 'launch/laser/laser.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'laser_model': laser_model,
            'laser_id': laser_id,
            'laser_uri': laser_uri,
            'laser_max_angle': laser_max_angle,
            'laser_min_angle': laser_min_angle,
        }.items()
    )

    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_devices'), 'launch/camera/camera.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'camera_model': camera_model,
            'camera_id': camera_id,
            'camera_uri': camera_uri,
        }.items()
    )

    group = GroupAction([
        PushRosNamespace(LaunchConfiguration('robot_id')),
        laser,
        camera
    ])

    return LaunchDescription(declared_arguments + [group])