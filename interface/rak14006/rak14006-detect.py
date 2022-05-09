#!/usr/bin/env python3
"""
RAK14006 rotary encoder example,outputs the position of the encoder and button press.
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import gpiod
from datetime import timedelta

'''
If you mount RAK14006 on the Pi-HAT(RAK6421) IO slot 1, the Counter Clockwise(CCW) pin is 16 
and Clockwise(CW) pin is 12, Button Switch(SW) pin is 6. 
If you use mount RAK14006 to Pi-HAT(RAK6421) IO slot 2, change CCW_PIN to 24,  CW_PIN to 22, SW_PIN to 21.
'''
CCW_PIN = 16
CW_PIN = 12
SW_PIN = 6
# position is 0 when start up
position = 0
# gpiochip0 [pinctrl-bcm2711] (58 lines)
chip = gpiod.chip(0)

ccw_line = chip.get_line(CCW_PIN)
cw_line = chip.get_line(CW_PIN)
sw_line = chip.get_line(SW_PIN)

config = gpiod.line_request()
config.request_type = gpiod.line_request.EVENT_RISING_EDGE
ccw_line.request(config)
cw_line.request(config)

config.request_type = gpiod.line_request.EVENT_FALLING_EDGE
sw_line.request(config)

try:
    while True:
        if ccw_line.event_wait(timedelta(seconds=0.1)):
            event = ccw_line.event_read()
            if event.event_type == gpiod.line_event.RISING_EDGE:
                position -= 1
                print("position step is %d" % position)
        if cw_line.event_wait(timedelta(seconds=0.1)):
            event = cw_line.event_read()
            if event.event_type == gpiod.line_event.RISING_EDGE:
                position += 1
                print("position step is %d" % position)
        if sw_line.event_wait(timedelta(seconds=0.1)):
            event = sw_line.event_read()
            if event.event_type == gpiod.line_event.FALLING_EDGE:
                print("button press")

except KeyboardInterrupt:
    print("ctrl+c...")
    exit()
