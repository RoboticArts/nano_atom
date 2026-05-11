#!/bin/bash

tmux kill-session -t nano_atom

#if $ROBOT_RUN_SIMULATION 
#then
  pkill -9 -f "gz sim"
#fi