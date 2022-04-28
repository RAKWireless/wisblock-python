#!/usr/bin/env python3
"""
Monitor the RAK12006 PIR (Pyroelectric Infrared Radial) using interrupts and outputs an alert when movement is detected
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import gpiod
from datetime import timedelta

# if RAK12006 is mounted on Pi-HAT slot 1, the enable pin is 12, which is GPIO 12 (board pin 32)
# if RAK12006 is mounted on Pi-HAT slot 2, the enable pin is 22, which is GPIO 22 (board pin 15)
digital_out_pin = 12
# digital_out_pin = 22

# gpiochip0 is the default gpiochip on bcm2711]
chip = gpiod.chip(0)
digital_out_line = chip.get_line(digital_out_pin)
config = gpiod.line_request()
# set the consumers of the lines
config.consumer = "RAK12006 PIR"
# Set request type to detect rising and falling edges
config.request_type = gpiod.line_request.EVENT_BOTH_EDGES
digital_out_line.request(config)

try:
    while True:
        if digital_out_line.event_wait(timedelta(seconds=1)):
            event = digital_out_line.event_read()
            if event.event_type == gpiod.line_event.RISING_EDGE:
                print("IR detected ...")
            if event.event_type == gpiod.line_event.FALLING_EDGE:
                print("No motion.")
except KeyboardInterrupt:
    print("ctrl+c...")
    exit()
