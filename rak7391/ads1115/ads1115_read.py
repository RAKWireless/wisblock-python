#!/usr/bin/env python3
"""
Read the specified ADC channel using the set gain value.
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "0.1.0"
__status__ = "Production"

import time
import Adafruit_ADS1x15

'''
ads1115 using an I2C communication bus
'''
ADS1115_BUS = 0x1
ADS1115_ADDRESS = 0x48

'''
set a gain of 1 for reading voltages from 0 to 4.09V.
Or pick a different gain to change the range of voltages that are read:
  - 2/3 = +/-6.144V
  -   1 = +/-4.096V
  -   2 = +/-2.048V
  -   4 = +/-1.024V
  -   8 = +/-0.512V
  -  16 = +/-0.256V
'''
ADS1115_GAIN = 1
ADS1115_CHANNEL = 0
SAMPLE_NUM = 32

# Create an ADS1115 ADC (16-bit) instance.

adc = Adafruit_ADS1x15.ADS1115(address=ADS1115_ADDRESS, busnum=ADS1115_BUS)

for i in range(0, SAMPLE_NUM):
	'''
	This value is a number that ranges from -32768 to 32767 on the 16-bit ADS1115,
    A value of 0 means the signal is at a ground (reference) level, 32767  means 
    it's at or higher than the maximum voltage value for the current gain.
	'''
	value = adc.read_adc(ADS1115_CHANNEL, gain=ADS1115_GAIN)
	print(value)
	time.sleep(0.5)

