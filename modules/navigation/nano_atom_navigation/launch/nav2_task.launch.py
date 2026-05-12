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
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.actions import GroupAction
from launch_ros.parameter_descriptions import ParameterFile

def generate_launch_description():
    
    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    use_sim = LaunchConfiguration("use_sim")

    # Nav2 core node configurations

    controller_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/controller_server.yaml'
        ]),
        allow_substs=True,
    )

    planner_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/planner_server.yaml'
        ]),
        allow_substs=True,
    )

    # Nav2 auxiliary node configurations

    behavior_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/behavior_server.yaml'
        ]),
        allow_substs=True,
    )

    smoother_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/smoother_server.yaml'
        ]),
        allow_substs=True,
    )

    # Nav2 orchestration node configurations

    bt_navigator_config = ParameterFile(
        PathJoinSubstitution([
            FindPackageShare("nano_atom_navigation"),
            'config/bt_navigator.yaml'
        ]),
        allow_substs=True,
    )

    bt_navigator_pose_xml = PathJoinSubstitution([
        FindPackageShare('nano_atom_navigation'),
        'config/behavior_trees/navigate_to_pose.xml'
    ])

    bt_navigator_poses_xml = PathJoinSubstitution([
        FindPackageShare('nano_atom_navigation'),
        'config/behavior_trees/navigate_through_poses.xml'
    ])

    # Nav2 core nodes

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[controller_config, {'use_sim_time': use_sim}],
        remappings=[
            ('cmd_vel', 'robot_base_controller/cmd_vel'),
            ('odom', 'robot_base_controller/odom'),
        ]
    )

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[planner_config, {'use_sim_time': use_sim}],
    )

    # Nav2 auxiliary nodes

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[behavior_config, {'use_sim_time': use_sim}],
        remappings=[
            ('cmd_vel', 'robot_base_controller/cmd_vel')
        ] 
    )

    smoother_server = Node(
        package='nav2_smoother',
        executable='smoother_server',
        name='smoother_server',
        output='screen',
        parameters=[smoother_config, {'use_sim_time': use_sim}],
    )

    # Nav2 orchestration nodes

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[
            bt_navigator_config,
            {
                'use_sim_time': use_sim,
                'default_nav_to_pose_bt_xml': bt_navigator_pose_xml,
                'default_nav_through_poses_bt_xml': bt_navigator_poses_xml,
            }
        ],
        remappings=[
            ('odom', 'robot_base_controller/odom'),
        ]
    )
   
    lifecycle_manager_navigation = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[
            {
                'use_sim_time': use_sim,
                'autostart': True,
                'node_names': [
                    'controller_server',
                    'planner_server',
                    'behavior_server',
                    'smoother_server',
                    'bt_navigator'
                ]
            }
        ]
    )

    group = GroupAction([
        controller_server,
        planner_server,
        behavior_server,
        smoother_server,
        bt_navigator,
        lifecycle_manager_navigation
    ])

    return LaunchDescription([group])