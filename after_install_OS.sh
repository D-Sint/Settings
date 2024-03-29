#!/usr/bin/bash

#!/bin/bash

file_path="~/after_intsall_OS.sh"

if [ -f "$file_path" ]; then
    echo "File exists"
else
    git clone https://github.com/D-Sint/Settings/after_install_OS.sh ~/
fi

echo "Install neccessary packages"
sudo apt install curl wget tree htop ripgrep conky-all git zsh -y

# add repo for vim
sudo add-apt-repository ppa:jonathonf/vim

sudo apt update

#install vim
sudo apt install vim vim-python-jedi -y 

# install vundle
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

# install ycm
git clone https://github.com/Valloric/YouCompleteMe.git ~/.vim/bundle/YouCompleteMe

# install clang
sudo apt install clang

# install vim-wombat
git clone git@github.com:michalbachowski/vim-wombat256mod.git && cd vim-wombat256mod && cp colors/wombat256mod.vim ~/.vim/colors 


# install crow-translate
sudo add-apt-repository ppa:jonmagon/crow-translate

sudo apt update && sudo apt install crow-translate && sudo apt upgrade -y

if [ -e $HOME/.oh-my-zsh ]; then
  rm -r $HOME/.oh-my-zsh
fi

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# change shell to zsh
echo "change shell on zsh"
chsh -s $(which zsh)

# change language to UA
echo "setup language UA"
if locale -a | grep uk_UA;then
  export LANG=uk_UA.utf-8
fi

echo "setup vim/vundle [don't miss setup YCM/reload it]"
time 5
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
echo "please install plugins INSIDE VIM. After this install clang-completer for YCM\
  and restart it."
vim

echo "Install YCM --clang-completer"
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --clang-completer
vim
