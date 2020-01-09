#!/usr/bin/env python3
import math
import os
import subprocess
import time


def sensor():

    Light_Blue = '%{F#66d9ef}'
    color_start = '%{F#a6e22e}'
    color_end = '%{F-}'
    CPUTEMP = 'cputemp'
    FANSPEED = 'fanspd'
    GET_TEMP = subprocess.run(
            [CPUTEMP],
            capture_output=True,
            text=True
            )
    TEMP = int(GET_TEMP.stdout)
    GET_FANSPEED = subprocess.run(
            [FANSPEED],
            capture_output=True,
            text=True
            )
    TEMP = int(GET_TEMP.stdout)
    SPEED = int(GET_FANSPEED.stdout)
    temp = int(TEMP)
    speed = int(SPEED)
    icon_fan = ''
    icon_temp = ''
    sp = str(speed)
    te = str(temp)
    output = subprocess.run(['polify', '--module', 'autofan', color_start, icon_fan, color_end, sp, color_start, icon_temp, color_end, te,'°C'], capture_output=True)

kh:quit(:quit(f

    A = 0

    if temp < 40:
        A = 0
        B += 0
        mode = f"{A} {B}"
    A = 0
    B = 0
    if temp >= 40:
        A = 0
        B += 1
        mode = f"{A} {B}"
    A = 0
    B = 0
    if temp >= 50:
        A += 1
        B += 1
        mode = f"{A} {B}"
    A = 0
    B = 0
    if temp >= 60:
        A += 2
        B += 1
        mode = f"{A} {B}"
    A = 0
    B = 0
    if temp > 65:
        A += 2
        B += 2
        mode = f"{A} {B}"
    i8kfan = "i8kfan "
    control = i8kfan + mode
    os.popen(control)
    output



def autofan():
    x = 1
    while x == 1:
        sensor()
        time.sleep(3)


autofan()

