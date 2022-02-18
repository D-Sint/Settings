set nocompatible
filetype off

"=====================================================
" Vundle settings
"=====================================================
" set the runtime path to include Vundle and initialize
set rtp+=/home/sint/.vim/bundle/Vundle.vim

call vundle#begin()

" This is the Vundle package, which can be found on GitHub.
" For GitHub repos, you specify plugins using the
" 'user/repository' format
Plugin 'gmarik/Vundle.vim'


"---------=== Code/project navigation ===-------------
" We could also add repositories with a ".git" extension
Plugin 'preservim/nerdtree' 	   " Project and file navigation

"---------------=== Languages support ===-------------
" --- Python ---
Plugin 'Valloric/YouCompleteMe'    " Autocomplete
Plugin 'jmcantrell/vim-virtualenv' " User virtualenv for current python interpretator
Plugin 'nvie/vim-flake8'           " Linter for python code

" --- HTML ---
Plugin 'mattn/emmet-vim' 	   " Autocomplete tags HTML


call vundle#end()

"Stick this in your vimrc to open NERDTree with `Ctrl+n`
" (you can set whatever key you want):
map <C-n> :NERDTreeToggle<CR>	   " Open/Close NerdTree
" Aoutoclose after open file
let NERDTreeQuitOnOpen=1

" Remap keys for EMMET
let g:user_emmet_leader_key='<C-Z>'

" Now we can turn our filetype functionality back on
"
filetype on
filetype plugin on
filetype plugin indent on
set number
syntax on
set linespace=3
set encoding=utf-8
