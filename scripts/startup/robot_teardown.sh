#!/bin/bash

tmux kill-session -t nano_atom

# Check if gz sim is running
# wait until is killed
#if $ROBOT_RUN_SIMULATION 
#then
  pkill -9 -f "gz sim"
#fi
sleep 3.0