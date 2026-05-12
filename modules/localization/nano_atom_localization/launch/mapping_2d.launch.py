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

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import GroupAction
from launch_ros.parameter_descriptions import ParameterFile

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    laser_topic = LaunchConfiguration("laser_topic")
    use_sim = LaunchConfiguration("use_sim")

    slam_toolbox_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_localization"),
            'config/slam_toolbox.yaml'
        ]),
        allow_substs=True,
    )

    slam_toolbox_mapping = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox_mapping',
        output='screen',
        parameters=[
            slam_toolbox_config,
            {
                'use_sim_time': use_sim,
                'use_lifecycle_manager': True,
            }
        ],
        remappings=[
            ('/map', 'map')  # Remap to a relative topic within the robot namespace
        ]
    )

    lifecycle_manager_mapping = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_mapping',
        output='screen',
        parameters=[
            {
                'use_sim_time': use_sim,
                'autostart': True,
                'node_names': ['slam_toolbox_mapping'],
                'bond_timeout': 4.0
            }
        ]
    )

    group = GroupAction([
        slam_toolbox_mapping,
        lifecycle_manager_mapping
    ])

    return LaunchDescription([group])