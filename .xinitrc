#!/usr/bin/env sh

[ -f "$HOME/.xprofile" ] && . ~/.xprofile

xset +fp /home/michael/.local/share/fonts

xset fp rehash


exec i3
