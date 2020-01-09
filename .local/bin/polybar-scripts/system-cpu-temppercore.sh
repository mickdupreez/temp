#!/bin/sh

sensors | grep Core | awk '{print "%{F#a6e22e}%{F-}" substr($3, 2, length($3)-5)}' | tr "\\n" " " | sed 's/ /°C  /g' | sed 's/  $//'
