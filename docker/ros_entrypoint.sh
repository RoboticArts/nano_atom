#!/bin/bash
set -e

# Source ROS2
source /opt/ros/${ROBOT_DISTRO}/setup.bash
source ${ROBOT_WS}/install/setup.bash

exec "$@"