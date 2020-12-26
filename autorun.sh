#!/bin/bash


# Refresh rate
xrandr -s 2560x1080 -r 100 &&

# Lights for keyboard and mouse
ckb-next &&

# Wallpaper
feh --bg-fill .config/qtile/background.jpg

