#!/bin/sh

HOST=1.1.1.1

if ! ping=$(ping -n -c 1 -W 1 $HOST); then
    echo " ping failed"
else
    rtt=$(echo "$ping" | sed -rn 's/.*time=([0-9]{1,})\.?[0-9]{0,} ms.*/\1/p')

    if [ "$rtt" -lt 50 ]; then
        icon="%{F#a6e22e}%{F-}"
    elif [ "$rtt" -lt 150 ]; then
        icon="%{F#a6e22e}%{F-}"
    else
        icon="%{F#a6e22e}%{F-}"
    fi

    echo "$icon $rtt ms"
fi
