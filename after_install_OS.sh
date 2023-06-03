#!/usr/bin/bash

sudo apt install tree htop vim vim-python-jedi ripgrep conky-all -y

sudo apt install git zsh -y

# install crow-translate
sudo add-apt-repository ppa:jonmagon/crow-translate

sudo apt update && sudo apt install crow-translate && sudo apt upgrade -y

if [ -e $HOME/.oh-my-zsh ]; then
  rm -r $HOME/.oh-my-zsh
fi

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# change shell to zsh
chsh -s $(which zsh)

# change language to UA
if locale -a | grep uk_UA;then
  export LANG=uk_UA.utf-8
fi

