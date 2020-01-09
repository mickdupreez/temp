#!/bin/sh

speed=$(sensors | grep fan1 | cut -d " " -f 9)

if [ "$speed" != "" ]; then
    speed_round=$(echo $speed %{F#a6e22e}RPM%{F-} )
    echo ""%{F#a6e22e}%{F-}" $speed_round"
else
   echo "%{F#a6e22e}%{F-} OFF"
fi
