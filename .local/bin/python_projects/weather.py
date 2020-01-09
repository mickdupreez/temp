#!/usr/bin/env python3

import subprocess
import time




def weather():
    cmd = 'weathercom'
    temp = subprocess.run([cmd], capture_output=True, text=True)

    subprocess.run(['polify', '--module', 'weather', temp.stdout])

weather()
