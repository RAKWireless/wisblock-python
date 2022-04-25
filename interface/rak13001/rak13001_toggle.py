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
from PCA95XX import PCA95XX_GPIO
import gpiod

#if you mount rak13001 on the RAK7391 Wisblock Connecter, run the code below 
I2C_BUS = 1
I2C_ADDRESS = 0x21

#if you use Wisblock Slot#1, relay pin number is 4, if you use Slot#2, change pin number to 12. 
WISBLOCK_RELAY_PIN = 4

I2C_BUS = 1
I2C_ADDRESS = 0x21
    
chip = PCA95XX_GPIO(I2C_BUS, I2C_ADDRESS, 16) 			
chip.setup(WISBLOCK_RELAY_PIN, PCA95XX_GPIO.OUT)

try:
    while True:
        chip.output(WISBLOCK_RELAY_PIN, 0)
        time.sleep(5)
        chip.output(WISBLOCK_RELAY_PIN, 1)
        time.sleep(5)
except:
    print('ctrl + c:')
    exit()

#else if you use rak13001 with WisBlock Pi Hat, plese run the code below 
 
'''
#if you use IO Slot 1, relay pin number is 16, if you use IO Slot 2, change pin number to 24
PI_HAT_RELAY_PIN = 16

chip = gpiod.chip(0)
line = chip.get_line(PI_HAT_RELAY_PIN)
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
'''
