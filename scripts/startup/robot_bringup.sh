#!/bin/bash

export ROBOT_WORKSPACE=$HOME/ros2_ws

# Find the first parent directory that looks like a ROS workspace.
find_workspace() {
  local dir="$1"
  while [[ "$dir" != "/" ]]; do
    [[ -d "$dir/build" && -d "$dir/install" && -d "$dir/log" && -d "$dir/src" ]] && {
      printf '%s\n' "$dir"
      return 0
    }
    dir="$(dirname "$dir")"
  done
  return 1
}

if [[ ! -d "$ROBOT_WORKSPACE" ]]; then
  printf '\033[33m[WARN] Workspace path not found: %s. Searching for a valid one...\033[0m\n' "$ROBOT_WORKSPACE"
  workspace_path="$(find_workspace "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)")" || {
    echo -e '\033[31m[ERROR] Path does not exist: %s\033[0m\n' "$ROBOT_WORKSPACE"
    echo -e '\033[31m[ERROR] No valid workspace was found and the script will exit.\033[0m'
    exit 1
  }
  printf '\033[33m[WARN] Workspace found: %s\033[0m\n' "$workspace_path"
  export ROBOT_WORKSPACE="$workspace_path"
fi

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


run_tmux "base" "mon2 launch --session base nano_atom_base base.launch.py"

if $ROBOT_RUN_DEVICES && ! $ROBOT_USE_SIM;
then
  run_tmux "devices" "mon2 launch --session devices nano_atom_devices devices.launch.py" true
fi

if $ROBOT_RUN_LOCALIZATION
then
  run_tmux "localization" "mon2 launch --session localization nano_atom_localization localization.launch.py" true
fi

if $ROBOT_RUN_NAVIGATION 
then
  run_tmux "navigation" "mon2 launch --session navigation nano_atom_navigation navigation.launch.py" true
fi


tmux attach -t $SESSION_NAME