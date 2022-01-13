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
IO2_1		= 17
IO2_2   	= 18
OC_PIN		= IO2_1 
RELAY_PIN	= IO2_2

bus = SMBus(I2C_BUS)

def set_bit(value, bit):
	return value | (1 << bit)


def clear_bit(value, bit):
	return value & ~(1 << bit)

def set_high(pin):
	write_value = bus.read_i2c_block_data(I2C_ADDR, 0, 3)
	#print(write_value)
	
	if pin in range(0, 8):
		write_value[0] = set_bit((write_value[0]), 7 - pin)
	elif pin in range(8, 16):
		write_value[1] = set_bit((write_value[1]), 15 - pin)
	elif pin in range(16, 25):
		write_value[2] = set_bit((write_value[2]), 23 - pin)

	#print(write_value)
	bus.write_i2c_block_data(I2C_ADDR, 0, write_value)

def set_low(pin):
	write_value = bus.read_i2c_block_data(I2C_ADDR, 0, 3)
	#print(write_value)

	if pin in range(0, 8):
		write_value[0] = clear_bit((write_value[0]), 7 - pin)
	elif pin in range(8, 16):
		write_value[1] = clear_bit((write_value[1]), 15 - pin)
	elif pin in range(16, 25):
		write_value[2] = clear_bit((write_value[2]), 23 - pin)

	#print(write_value)
	bus.write_i2c_block_data(I2C_ADDR, 0, write_value)

try:
	count = 0
	while True:
		if count % 2 == 0:
			set_low(RELAY_PIN)
			print("turn off")
		else:
			set_high(RELAY_PIN)
			print("turn on")
		count += 1
		time.sleep(0.5)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    exit()


