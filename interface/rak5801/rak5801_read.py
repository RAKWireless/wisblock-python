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
import Adafruit_ADS1x15
import gpiod

GAIN = 1
SAMPLE_NUM = 32

# AIN0 cannot be used as an analog input channel by default

# WisBlock Slot#1: AIN0 = 0, AIN1 = 1, ENABLE_PIN = 17
# WisBlock Slot#2: AIN0 = 2, AIN1 = 3, ENABLE_PIN = 25

# RAK7391 IO Slot#1: AIN0 = 0, AIN1 = 1, ENABLE_PIN = 13
# RAK7391 IO Slot#2: AIN0 = 2, AIN1 = 3, ENABLE_PIN = 14


AIN0 = 0
AIN1 = 1
ENABLE_PIN = 17

# set enable pin to high
#
# If RAK5801 is connected to the native 40-pin header, chip = gpiod.chip(0); If RAK5801 is connected to a GPIO
# expander, use "gpiodetect" to find the gpio expander's gpiochip number, for example, chip = gpiod.chip(2)
chip = gpiod.chip(0)
line = chip.get_line(ENABLE_PIN)
config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
line.request(config)
line.set_value(1)

"""
reading rak5801 analog input via ads115 module 
"""
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
try:
    while True:
        total = 0
        for i in range(0, SAMPLE_NUM):
            # read rak5801 analog input 1
            value = adc.read_adc(AIN1, gain=GAIN)
            total += value
        raw = total / SAMPLE_NUM
        """
		This is a number that ranges from -32768 to 32767 on the 16-bit ADS1115,
		A value of 0 means the signal is at a ground (reference) level, 32767  means 
		it's at or higher than the maximum voltage value for the current gain (4.096V by default),
		"""
        voltage = raw * 4.096 / 32767;
        # I=U/149.9(mA)
        current = voltage / 149.9 * 1000;
        print("%.2f mA" % current)

except KeyboardInterrupt:
    print('ctrl + c:')
    exit()
