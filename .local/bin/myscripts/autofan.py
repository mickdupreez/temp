#!/usr/bin/env python3
import math
import os
import subprocess
import time






def fan_mode(fan1, fan2):
    i8kfan = "i8kfan"
    fan = f"'{'sudo'}' '{i8kfan}' '{fan1}' '{fan2}'"
    os.popen(fan)
    return int(fan1), int(fan1)

def temp_zone():
    icon1 = ''
    icon2= ''
    GRE = '%{F#a6e22e}'
    EN = '%{F-}'
    zone_1 = range(0, 40)
    zone_2 = range(39, 45)
    zone_3 = range(44, 55)
    zone_4 = range(54, 60)
    zone_5 = range(59, 120)

    cpu_temp = subprocess.run(['cputemp'],
            capture_output=True, text=True)
    fan_speed = subprocess.run(['fanspd'],
            capture_output=True, text=True)
    cpu = int(cpu_temp.stdout.rstrip())
    while cpu in range(0, 100):
        temp = int(cpu_temp.stdout)
        speed = int(fan_speed.stdout)
        output = print(GRE, icon1, EN, temp, GRE, icon2, EN, speed)
        SPEED = f'{speed}'
        TEMP = f'{temp}{"°C"}'
        run = subprocess.run(['polify', '--module', 'autofan',
            GRE, icon1, EN, SPEED,
            GRE, icon2, EN, TEMP])


        if temp in zone_5:
            print(5)
            fan_mode(fan1=2, fan2=2)
            run
            output
            break

        elif temp in zone_4:
            print(4)
            fan_mode(fan1=2, fan2=1)
            run
            output
            break


        elif temp in zone_3:
            print(3)
            fan_mode(fan1=1, fan2=1)
            run
            output
            break


        elif temp in zone_2:
            print(2)
            fan_mode(fan1=0, fan2=1)
            run
            output
            break


        elif temp in zone_1:
            print(1)
            fan_mode(fan1=0, fan2=0)
            run
            output
            break

        else:
            break

b = 1
while b == 1:
    temp_zone()
    time.sleep(3)
