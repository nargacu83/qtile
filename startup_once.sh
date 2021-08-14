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
  feh --bg-fill $HOME/.config/wallpaper/background.jpg
fi

#start polkit
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

#start notification-daemon
if [ -x "$(command -v dunst)" ]; then
  dunst &
fi

# # start file manager daemon
# if [ -x "$(command -v pcmanfm)" ]; then
#   pcmanfm -d &
# fi

#set redshift for night light
if [ -x "$(command -v redshift)" ]; then
  redshift &
fi

#start pamac-tray
# if [ -x "$(command -v pamac-tray)" ]; then
#   pamac-tray &
# fi


#set ckb-next for mouse dpi and devices lights
# if [ -x "$(command -v ckb-next)" ]; then
#   ckb-next &
# fi
