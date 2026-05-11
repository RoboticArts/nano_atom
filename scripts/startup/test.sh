tmux new-session -d -s nano_atom -n bringup

# Pane 1
tmux send-keys "ls" C-m

# Pane 2
tmux split-window -h
tmux send-keys "ls" C-m

# Pane 3
tmux split-window -v
tmux send-keys "ls" C-m

# Seleccionar layout limpio
tmux select-layout tiled

tmux attach