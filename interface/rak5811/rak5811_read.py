#!/usr/bin/env python3
"""
Reads values from a 0-5v sensor using a RAK5811 module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
import Adafruit_ADS1x15
import gpiod


GAIN = 1
SAMPLE_NUM = 32

# RAK6421 IO Slot#1: CHIP_NUM = 0, AIN1 = 1, ENABLE_PIN = 17
# RAK6421 IO Slot#2: CHIP_NUM = 0, AIN1 = 3, ENABLE_PIN = 25
# RAK7391 IO Slot#1: CHIP_NUM = 3, AIN1 = 1, ENABLE_PIN = 1
# RAK7391 IO Slot#2: CHIP_NUM = 3, AIN1 = 3, ENABLE_PIN = 9

CHIP_NUM = 3
AIN1 = 1
ENABLE_PIN = 1

# set rak5811 enable pin to high
chip = gpiod.chip(CHIP_NUM)
line = chip.get_line(ENABLE_PIN)
config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
line.request(config)
line.set_value(1)


"""
reading rak5811 analog input via ads115 module 
"""
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
try:
	while True:
		total = 0
		for i in range(0,SAMPLE_NUM):
			# read rak5811 analog input 1
			value = adc.read_adc(AIN1, gain=GAIN)
			total += value
		raw = total / SAMPLE_NUM
		"""
		This is a number that ranges from -32768 to 32767 on the 16-bit ADS1115,
		A value of 0 means the signal is at a ground (reference) level, 32767  means 
		it's at or higher than the maximum voltage value for the current gain (4.096V by default),
		"""
		voltage = raw * 4.096 / 32767;
		#Input signal reduced to 6/10 and output
		raw_voltage = voltage / 0.6 
		print("%.2f v"%raw_voltage)

except KeyboardInterrupt:
    print('ctrl + c:')
    exit()
