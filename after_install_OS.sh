#!/usr/bin/bash
git clone https://github.com/D-Sint/Settings/after_install_OS.sh ~/

echo "Install neccessary packages"
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
echo "change shell on zsh"
chsh -s $(which zsh)

# change language to UA
echo "setup language UA"
if locale -a | grep uk_UA;then
  export LANG=uk_UA.utf-8
fi

echo "setup vim/vundle [don't miss setup YCM/reload it]"
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
echo "please install plugins INSIDE VIM. After this install clang-completer for YCM\
  and restart it."
vim

echo "Install YCM --clang-completer"
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --clang-completer
vim
