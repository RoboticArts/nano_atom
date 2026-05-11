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
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, GroupAction

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    use_sim = LaunchConfiguration("use_sim")
    camera_model = LaunchConfiguration("camera_model")
    camera_id = LaunchConfiguration("camera_id")
    camera_uri = LaunchConfiguration("camera_uri")

    robot_prefix = PythonExpression(["'", robot_id, "/'"])

    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('nano_atom_devices'), 'launch/camera', 
                 PythonExpression(["'", camera_model, ".launch.py'"]),
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'camera_id': camera_id,
            'camera_uri': camera_uri,
        }.items()
    )

    group = GroupAction([
        camera
    ])

    return LaunchDescription([group])