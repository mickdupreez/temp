#!/usr/bin/env python3
from i3ipc import Connection, Event
from subprocess import call
import os
i3 = Connection()
th = 'polybar-msg hook titlehook 1'
show = 'polybar-msg cmd show'
hide = 'polybar-msg cmd hide'
bh = 'polybar-msg hook backupd 1'
ws = 'polybar-msg hook wshook 1'
ws1 = 'polybar-msg hook wshook1 1'


def windownotify(i3, event):
   # if event.container.fullscreen_mode == 0:
   #     os.system(show)
   #     #call('polybar-msg cmd show'.split(' '))
   # else:
   #     os.system(hide)
   #     #call('polybar-msg cmd hide'.split(' '))


    if event.change in "focus" "title":
        os.system(th)
        #call('polybar-msg hook titlehook 1'.split(' '))


    if event.change in "focus" "title":
        os.system(bh)
        #call('polybar-msg hook backupd 1'.split(' '))



def wsnotify(i3, event):
    if event.change in "focus":
        if event.old.num != -1:
            os.system(ws)
            #call('polybar-msg hook wshook 1'.split(' '))

def wsnotify1(i3, event):
    if event.change in "focus":
        if event.old.num != -1:
            os.system(ws1)


i3.on('window', windownotify)
i3.on('workspace', wsnotify)
i3.on('workspace', wsnotify1)

i3.main()
