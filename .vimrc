set nocompatible
filetype off

"=====================================================
" Vundle settings
"=====================================================
" set the runtime path to include Vundle and initialize
"
set rtp+=$HOME/.vim/bundle/Vundle.vim

call vundle#begin()

" This is the Vundle package, which can be found on GitHub.
" For GitHub repos, you specify plugins using the
" 'user/repository' format
Plugin 'gmarik/Vundle.vim'

"---------=== Code/project navigation ===-------------
" We could also add repositories with a ".git" extension
"
Plugin 'preservim/nerdtree'		  " Project and file navigation

"---------------=== Languages support ===-------------

" --- Python ---
"
Plugin 'Valloric/YouCompleteMe'		  " Autocomplete
Plugin 'jmcantrell/vim-virtualenv'	  " User virtualenv for current python interpretator
Plugin 'nvie/vim-flake8'		  " Linter for python code
Plugin 'Vimjas/vim-python-pep8-indent'	  " PEP8 indent

" --- HTML ---
"
Plugin 'mattn/emmet-vim'		  " Autocomplete tags HTML

" --- Vue ---
"Plugin 'leafOfTree/vim-vue-plugin'	  " Syntax highlighting and identaion for .vue files
"Plugin 'iloginow/vim-vue'		  " Syntax highlighting indentaion and autocomplete based on <template> <script> and <style> tags

call vundle#end()

" --------------- Python SETTINGS ----------------
" !python3 % executed for the current file with Python.
nnoremap <f5> :w <CR>:!clear <CR>:!python3 % <CR>

" --------------- Colorscheme SETTINGS for DIFFERENT filetypes ----------------
"autocmd BufEnter *.py	 colorscheme darcula
"autocmd BufEnter *.html  colorscheme wombat256mod

"Stick this in your vimrc to open NERDTree with `Ctrl+n`
" (you can set whatever key you want):
map <C-n> :NERDTreeToggle<CR>	   " Open/Close NerdTree
" Autoclose after open file
let NERDTreeQuitOnOpen=1
" Refresh NERDTree files and dirs
nmap <Leader>r :NERDTreeFocus<cr>R<c-w><c-p>

" Remap keys for EMMET
let g:user_emmet_leader_key='<C-x>'

" Global config file for every cpp extentions for YCM
" (no need to create 'ycm_extra_conf.py' in every project)
let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'

"Close autohint-window-preview for YCM 
set completeopt-=preview 
let g:ycm_add_preview_to_completeopt = 0

" ----------------- CPP settings --------------------
"
autocmd BufEnter *.cpp set shiftwidth=4


" Now we can turn our filetype functionality back on
"
filetype on
filetype plugin on
filetype plugin indent on
set number
colorscheme wombat256mod
syntax on
set linespace=3
set encoding=utf-8

set shiftwidth=2
set softtabstop=2
