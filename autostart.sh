#!/bin/bash
export SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

#set resolution and refresh rate
if [ -x "$(command -v xrandr)" ]; then
  xrandr -s 2560x1080 -r 100
fi

#boot picom if it exists
if [ -x "$(command -v picom)" ]; then
  picom &> /dev/null & 
fi

#set background
if [ -x "$(command -v feh)" ]; then
  feh --bg-fill $SCRIPTPATH/background.jpg
fi

#set redshift for night light
if [ -x "$(command -v xrandr)" ]; then
  redshift &
fi

#set ckb-next for mouse dpi and devices lights
if [ -x "$(command -v ckb-next)" ]; then
  ckb-next &
fi