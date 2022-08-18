#!/usr/bin/sh
SESSION="HTB"

tmux start-server

tmux new-session -d -s $SESSION

#Create 3 panels
tmux selectp -t 0
#tmux send-keys "pwd" C-m
tmux splitw -h -p 50

tmux selectp -t 1
tmux splitw -v -p 50

#tmux selectp -t 0

tmux attach-session -t $SESSION
