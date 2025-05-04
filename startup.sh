#!/bin/sh
# Startup script to load extras
#

xrandr --output eDP-1 --mode 1366x768 --pos 233x1080 --rotate normal --output DP-1 --off --output HDMI-1 --off --output HDMI-1-0 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1-0 --off --output DP-1-1 --off &
lxsession&
nitrogen --restore&
picom&
blueman-applet&
nm-applet&
dunst&
plank&
conky&
xprop -name plank -f _NET_WM_STATE 32a -set _NET_WM_STATE '_NET_WM_STATE_STICKY, _NET_WM_STATE_SKIP_TASKBAR, _NET_WM_STATE_SKIP_PAGER, _NET_WM_STATE_ABOVE'

