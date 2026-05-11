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
from launch.actions import OpaqueFunction, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch.actions import GroupAction, DeclareLaunchArgument
from launch_ros.actions import Node, PushRosNamespace
from pathlib import Path
import shutil

def find_workspace_root(start_path: Path) -> Path:
    """
    Goes up directory by directory until it finds one that contains 'install'.
    """
    current = start_path.resolve()
    while current != current.parent:  # until reaching the root 
        if (current / "install").exists():
            return current
        current = current.parent
    raise FileNotFoundError("No 'install' folder found at any upper level.")

def move_map(context, maps_path, map_folder_name):
    """
    Moves the map folder to the src of the automatically detected workspace.
    """
    maps_path = context.perform_substitution(maps_path)
    map_folder_name = context.perform_substitution(map_folder_name)

    map_folder = Path(maps_path) / map_folder_name
    if not map_folder.exists():
        raise FileNotFoundError(f"The folder {map_folder} does not exist: {map_folder}")

    # Automatically detect the workspace root
    workspace_root = find_workspace_root(Path(__file__))
    workspace_src = workspace_root / "src" / "maps"

    dest_folder = workspace_src / map_folder_name

    if dest_folder.exists():
        raise FileExistsError(f"The destination folder already exists: {dest_folder}")

    shutil.move(str(map_folder), str(dest_folder))
    return []

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
            "maps_path",
            default_value="/tmp",
            description="Path to the maps directory"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "map_name",
            default_value="demo_map",
            description="Name of the map to be saved"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    maps_path = LaunchConfiguration("maps_path")  
    map_name = LaunchConfiguration("map_name")

    # Map folder receives the same name as map_name
    map_folder_name = map_name

    create_map_folder = ExecuteProcess(
        cmd=['mkdir', '-p', [maps_path, '/', map_folder_name]],  # /tmp/demo_map
        shell=True
    )

    map_saver_cli = Node(
        package='nav2_map_server',
        executable='map_saver_cli',
        name='map_saver_cli',
        output='screen',
        parameters=[],
        arguments=[
            '-f', [maps_path, '/', map_folder_name, '/', map_name], # /tmp/demo_map/demo_map.file
            '--fmt', 'pgm',        # Map format                  
            '-t', "map"            # Map topic
        ]
    )

    move_map_action = OpaqueFunction(
        function=lambda context: move_map(context, maps_path, map_name)
    )

    move_after_save = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=map_saver_cli,
            on_exit=[move_map_action]
        )
    )

    group = GroupAction([
        PushRosNamespace(robot_id),
        create_map_folder,
        map_saver_cli,
        move_after_save
    ])

    return LaunchDescription(declared_arguments + [group])