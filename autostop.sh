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
#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

#set background
if [ -x "$(command -v feh)" ]; then
  feh --bg-scale $SCRIPTPATH/down.jpg
fi

echo "UnloadTheme" > $XDG_RUNTIME_DIR/leftwm/commands.pipe

pkill compton 
pkill picom
pkill polybar
pkill redshift