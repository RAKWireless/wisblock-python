#!/usr/bin/env python3
"""
Turns on and off the relay in the RAK13001
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
import gpiod

# Pi Hat: CHIP_NUM = 0, Slot#1: DO_PIN = 16, Slot#2: DO_PIN = 24
# WisBlock: CHIP_NUM =2, Slot#1: DO_PIN = 4, Slot#2: DO_PIN = 12 
CHIP_NUM = 0
DO_PIN = 16

chip = gpiod.chip(CHIP_NUM)
line = chip.get_line(DO_PIN)
config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
line.request(config)

try:
    while True:
        line.set_value(0)
        time.sleep(5)
        line.set_value(1)
        time.sleep(5)
except:
    print('ctrl + c:')
    exit()

