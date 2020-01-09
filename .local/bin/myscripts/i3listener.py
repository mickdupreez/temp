#!/usr/bin/env python3
from i3ipc import Connection, Event
from subprocess import call
import os
titlehook = Connection()
th = 'polybar-msg [-p pid] hook titlehook 1'
wh = 'polybar-msg hook weatherhook 1'
show = 'polybar-msg cmd show'
hide = 'polybar-msg cmd hide'
bh = 'polybar-msg hook backupd 1'
ws = 'polybar-msg hook wshook 1'



def windownotify(titlehook, event):
   # if event.container.fullscreen_mode == 0:
   #     os.system(show)
   #     #call('polybar-msg cmd show'.split(' '))
   # else:
   #     os.system(hide)
   #     #call('polybar-msg cmd hide'.split(' '))


    if event.change in "focus" "title":
        os.system(th)
        #call('polybar-msg hook titlehook 1'.split(' '))


titlehook.on('window', windownotify)


titlehook.main()

