session = "NOTES"
window=0
tmux start-server 
tmux new-session -d -s NOTES

#split windows
tmux splitw -h -p 50
tmux selectp -t 1
tmux splitw -v -p 50

tmux selectp -t 0
tmux send-keys -t NOTES "sudo apt update && sudo apt list --upgradable" C-m
tmux attach-session -t NOTES

