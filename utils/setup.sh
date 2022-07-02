#!/bin/bash

# --- fish ------
mkdir -p ~/.config/fish/conf.d/
cp ./fish/mytheme_colors.fish ~/.config/fish/conf.d/mytheme_colors.fish

mkdir -p ~/.config/fish/functions/
cp ./fish/fish_prompt.fish ~/.config/fish/functions/fish_prompt.fish

mkdir -p ~/.config/fish/
cp ./fish/config.fish ~/.config/fish/config.fish
# --- fish ------

# --- nvim ------
mkdir -p ~/.config/nvim/
cp ./nvim/init.vim ~/.config/nvim/init.vim
# --- nvim ------

# --- tmux ------
mkdir -p ~/bin/
cp ./tmux/ide.sh ~/bin/ide.sh
echo PATH="$PATH:~/bin" >> ~/.bashrc
source ~/.bashrc

cp ./tmux/.tmux.conf ~/.tmux.conf
# --- tmux ------
