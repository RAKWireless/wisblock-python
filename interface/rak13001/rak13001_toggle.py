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
import sys
import logging
from smbus2 import SMBus

I2C_ADDR 	= 0x20
I2C_BUS 	= 1
IO2_0		= 16
IO2_2   	= 18
OC_PIN		= IO2_0 
RELAY_PIN	= IO2_2

bus = SMBus(I2C_BUS)


def set_high():
	write_value = [0xff, 0xff, 0xff]
	bus.write_i2c_block_data(I2C_ADDR, 0, write_value)

def set_low():
	write_value = [0x0, 0x0, 0x0]
	bus.write_i2c_block_data(I2C_ADDR, 0, write_value)

try:
	count = 0
	while True:
		if count % 2 == 0:
			set_low()
			print("turn off")
		else:
			set_high()
			print("turn on")
		count += 1
		time.sleep(0.5)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    exit()

