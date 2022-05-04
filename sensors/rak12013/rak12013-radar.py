#!/usr/bin/env python3
"""
Detect motion with rak12016 radar sensor.
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import gpiod
from datetime import timedelta

'''
if you mount rak12016 on the PI-Hat IO slot 1, the enable pin is 16 and out pin is 13, 
if you use IO slot 2, change enable pin to 24 and out pin to 23.
'''
EN_PIN = 16
OUT_PIN = 13

chip = gpiod.chip(0)
en_line = chip.get_line(EN_PIN)
out_line = chip.get_line(OUT_PIN)

config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
en_line.request(config)
en_line.set_value(1)

config.request_type = gpiod.line_request.EVENT_BOTH_EDGES
out_line.request(config)

try:
    while True:
        if out_line.event_wait(timedelta(seconds=1)):
            event = out_line.event_read()
            if event.event_type == gpiod.line_event.RISING_EDGE:
                print("motion detected!")
            if event.event_type == gpiod.line_event.FALLING_EDGE:
                print("No motion.")
except KeyboardInterrupt:
    print("ctrl+c...")
    exit()

