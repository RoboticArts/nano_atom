#!/usr/bin/python3
# Copyright 2020, EAIBOT
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch.actions import GroupAction, SetLaunchConfiguration
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterFile

def generate_launch_description():
    
    laser_id = LaunchConfiguration("laser_id")
    laser_uri = LaunchConfiguration("laser_uri")
    laser_max_angle = LaunchConfiguration("laser_max_angle")
    laser_min_angle = LaunchConfiguration("laser_min_angle")

    laser_max_angle_deg = PythonExpression([
        "str(float(", laser_max_angle, ") * 180.0 / 3.14159265359)"
    ])

    laser_min_angle_deg = PythonExpression([
        "str(float(", laser_min_angle, ") * 180 / 3.14159265359)"
    ])

    lidar_params = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_devices"),
            "config/laser/ydlidar_x2.yaml"
        ]),
        allow_substs=True,
    )

    ydlidar = Node(
        package="ydlidar_ros2_driver",
        executable="ydlidar_ros2_driver_node",
        name=laser_id,
        output="screen",
        parameters=[lidar_params],
        remappings=[
            ('scan', ["/", laser_id, "/scan"]),
        ]
    )

    group = GroupAction([
        SetLaunchConfiguration("laser_max_angle_deg", laser_max_angle_deg),
        SetLaunchConfiguration("laser_min_angle_deg", laser_min_angle_deg),
        ydlidar
    ])

    return LaunchDescription([group])
