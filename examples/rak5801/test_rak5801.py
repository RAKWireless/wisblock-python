#!/usr/bin/env python3
"""
Reads values from a 4-20mA sensor using a RAK5801 module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
import sys
import logging
import Adafruit_ADS1x15

I2C_ADDRESS 	= 0x48
I2C_BUS 		= 0x1
GAIN 			= 2/3
ANALOG_INPUT_0 	= 0
ANALOG_INPUT_1 	= 1
SAMPLE_NUM		= 32
"""
reading rak5801 analog input via adc module 
"""
adc = Adafruit_ADS1x15.ADS1115(address=I2C_ADDRESS, busnum=I2C_BUS)
try:
	while True:
		total = 0
		for i in range(0,SAMPLE_NUM):
			# read rak5801 analog input 0
			value = adc.read_adc(ANALOG_INPUT_0, gain=GAIN)
			total += value
		result = total/SAMPLE_NUM
		print("%d"%result)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    exit()
