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
from launch.substitutions import LaunchConfiguration
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.actions import GroupAction
from launch_ros.parameter_descriptions import ParameterFile

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    use_sim = LaunchConfiguration("use_sim")

    waypoint_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/waypoint_follower.yaml'
        ]),
        allow_substs=True,
    )

    route_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/route_server.yaml'
        ]),
        allow_substs=True,
    )

    route_graph_filepath = PathJoinSubstitution([
        FindPackageShare('nano_atom_navigation'),
        'config/graph/demo_map_graph.geojson'
    ])

    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[waypoint_config, {'use_sim_time': use_sim}]
    )

    # Not available in Jazzy from apt
    route_server = Node(
        package='nav2_route',
        executable='route_server',
        name='route_server',
        output='screen',
        respawn_delay=2.0,
        parameters=[
            route_config,
            {
                'use_sim_time': use_sim,
                'graph_filepath': route_graph_filepath
            }
        ]
    )

    lifecycle_manager_mission_navigation = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_mission_navigation',
        output='screen',
        parameters=[
            {
                'use_sim_time': use_sim,
                'autostart': True,
                'node_names': [
                    'waypoint_follower',
                    #'route_server'
                ]
            }
        ]
    )

    group = GroupAction([
        waypoint_follower,
        #route_server,
        lifecycle_manager_mission_navigation,
    ])

    return LaunchDescription([group])
