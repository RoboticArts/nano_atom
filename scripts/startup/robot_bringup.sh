#!/bin/bash

export ROBOT_WORKSPACE=~/ros/ws/atom_ws
export ROBOT_FOLDER=${ROBOT_WORKSPACE}/src/nano_atom

SESSION_NAME="nano_atom"

echo '    _   _____    _   ______     ___  __________  __  ___'
echo '   / | / /   |  / | / / __ \   /   |/_  __/ __ \/  |/  /'
echo '  /  |/ / /| | /  |/ / / / /  / /| | / / / / / / /|_/ / '
echo ' / /|  / ___ |/ /|  / /_/ /  / ___ |/ / / /_/ / /  / /  '
echo '/_/ |_/_/  |_/_/ |_/\____/  /_/  |_/_/  \____/_/  /_/   '
echo '                                                         '
                                          
source $ROBOT_WORKSPACE/install/setup.bash
source $ROBOT_FOLDER/scripts/startup/robot_params.env

export ROSMON_COLOR_MODE=256colors
export DISPLAY=:0
export XAUTHORITY=/run/user/1000/gdm/Xauthority

# -----------------------------
# FUNCION TMUX
# -----------------------------
run_tmux() {
  local name="$1"
  local command="$2"
  local create_window="${3:-false}"

  if [[ "$create_window" == true ]]; then
    tmux new-window -t "$SESSION_NAME" -n "$name"
  fi

  tmux send-keys -t "$SESSION_NAME:$name" "source /opt/ros/$ROS_DISTRO/setup.bash" C-m
  tmux send-keys -t "$SESSION_NAME:$name" "source $ROBOT_WORKSPACE/install/setup.bash" C-m
  tmux send-keys -t "$SESSION_NAME:$name" "source $ROBOT_FOLDER/scripts/startup/robot_params.env" C-m
  tmux send-keys -t "$SESSION_NAME:$name" "echo 'Launching $name module...'" C-m
  tmux send-keys -t "$SESSION_NAME:$name" "$command" C-m

  sleep 1
}

# -----------------------------
# RESET SESSION
# -----------------------------

echo "Killing previous tmux session..."
./robot_teardown.sh

echo "Starting tmux session..."
tmux new-session -d -s $SESSION_NAME -n "base"

if [[ -z $ROBOT_AUTOBOOT ]]; then
   ROBOT_AUTOBOOT=false
fi

echo "USE SIM = $ROBOT_USE_SIM"

echo "RUN LOCALIZATION = $ROBOT_RUN_LOCALIZATION"
echo "RUN NAVIGATION = $ROBOT_RUN_NAVIGATION"


run_tmux "base" "ros2 launch nano_atom_base base.launch.py"

if $ROBOT_RUN_DEVICES && ! $ROBOT_USE_SIM;
then
  run_tmux "devices" "ros2 launch nano_atom_devices devices.launch.py" true
fi

if $ROBOT_RUN_LOCALIZATION
then
  run_tmux "localization" "ros2 launch nano_atom_localization localization.launch.py" true
fi

if $ROBOT_RUN_NAVIGATION 
then
  run_tmux "navigation" "ros2 launch nano_atom_navigation navigation.launch.py" true
fi


tmux attach -t $SESSION_NAME