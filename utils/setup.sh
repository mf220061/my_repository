#!/bin/bash

mkdir -p ~/.config/fish/conf.d/
cp ./fish/mytheme_colors.fish ~/.config/fish/conf.d/mytheme_colors.fish

mkdir -p ~/.config/fish/functions/
cp ./fish/fish_prompt.fish ~/.config/fish/functions/fish_prompt.fish

mkdir -p ~/.config/fish/
cp ./fish/config.fish ~/.config/fish/config.fish
