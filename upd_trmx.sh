#!/data/data/com.termux/files/usr/bin/bash

file_path="$HOME/after_install_OS.sh"

if [ -f "$file_path" ]; then
    echo "File exists"
else
    git clone https://github.com/D-Sint/Settings/after_install_OS.sh $HOME/
fi

echo "Install necessary packages"
pkg install curl wget tree htop ripgrep git zsh -y

# Install vim
pkg install vim-python -y

# Install Vundle
git clone https://github.com/VundleVim/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim

# Install YouCompleteMe
pkg install clang -y
git clone https://github.com/Valloric/YouCompleteMe.git $HOME/.vim/bundle/YouCompleteMe

# Install vim-wombat
git clone https://github.com/michalbachowski/vim-wombat256mod.git && cd vim-wombat256mod && cp colors/wombat256mod.vim $HOME/.vim/colors

# Install crow-translate
pkg install crow-translate -y

# Install Oh My Zsh
if [ -d "$HOME/.oh-my-zsh" ]; then
  rm -rf $HOME/.oh-my-zsh
fi
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Change shell to zsh
echo "Change shell to zsh"
chsh -s $(which zsh)

# Setup language to Ukrainian
echo "Setup language to Ukrainian"
export LANG=uk_UA.utf-8

# Setup vim/vundle
echo "Setup vim/vundle [don't miss setup YCM/reload it]"
sleep 5
git clone https://github.com/VundleVim/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim
echo "Please install plugins INSIDE VIM. After this install clang-completer for YCM and restart it."
vim

# Install YCM --clang-completer
echo "Install YCM --clang-completer"
cd $HOME/.vim/bundle/YouCompleteMe
python3 install.py --clang-completer

