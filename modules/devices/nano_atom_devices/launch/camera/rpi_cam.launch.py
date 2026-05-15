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

from launch.actions import GroupAction
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression

def generate_launch_description():
    
    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    camera_id = LaunchConfiguration("camera_id")
    camera_uri = LaunchConfiguration("camera_uri")

    camera_ros = Node(
        package="camera_ros",
        executable="camera_node",
        name=camera_id,
        output="screen",
        parameters=[{
            "camera": camera_uri,
            "frame_id": PythonExpression(["'", robot_prefix, "' + '", camera_id, "_rgb_optical_link'"]),
            "width": 640,
            "height": 480,
            "format": "",
        }],

    )

    group = GroupAction([
        camera_ros
    ])

    return LaunchDescription([group])