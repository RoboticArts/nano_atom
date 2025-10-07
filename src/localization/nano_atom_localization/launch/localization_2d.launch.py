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
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import GroupAction

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    use_sim = LaunchConfiguration("use_sim")

    map_file = PathJoinSubstitution([
        FindPackageShare('nano_atom_localization'),
        'maps/demo_map/demo_map.yaml'
    ])

    amcl_config = PathJoinSubstitution([
        FindPackageShare('nano_atom_localization'),
        'config/amcl.yaml'
    ])

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {
                'use_sim_time': use_sim,
                'yaml_filename': map_file
            }
        ]
    )
            
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            amcl_config,
            {
                'use_sim_time': use_sim,
            }
        ]
    )

    lifecycle_manager_localization = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters = [
            {
                'use_sim_time': use_sim,
                'autostart': True,
                'node_names': ['map_server', 'amcl']
            }
        ]
    )

    group = GroupAction([
        map_server,
        amcl,
        lifecycle_manager_localization
    ])

    return LaunchDescription([group])