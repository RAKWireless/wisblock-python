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
from smbus2 import SMBus
import json



GAIN 			= 1
# only analog input 1 can work now
ANALOG_INPUT_1 	= 1  
SAMPLE_NUM		= 32

PATH = '/etc/gpio_expander.json'

Port = ["IO0_0", "IO0_1", "IO0_2", "IO0_3", "IO0_4", "IO0_5", "IO0_6", "IO0_7",
            "IO1_0", "IO1_1", "IO1_2", "IO1_3", "IO1_4", "IO1_5", "IO1_6", "IO1_7",
            "IO2_0", "IO2_1", "IO2_2", "IO2_3", "IO2_4", "IO2_5", "IO2_6", "IO2_7"
]


def getPortNum(name):
	for i in range(0, 24):
		if Port[i] == name:
			return i

def write_value(name, value):

    if name not in Port:
        print("Invalid IO port name!")
        sys.exit()
    if value != 0 and value != 1:
        print("Invalid value to write!")
        sys.exit()

    save = {}
    with open(PATH,'rb') as f:
        cur = json.load(f)
        cur["status"][name] = value
        save = cur
    f.close()

    with open(PATH,'w') as r:
        json.dump(save,r)
    r.close()

    value = [0xff, 0xff, 0xff]

    for tmp in Port:

        if save["status"][tmp] == 0:
            num = getPortNum(tmp)
            if num in range(0, 8):
                value[2] &= ~(1 << num)
            if num in range(8, 16):
                value[1] &= ~(1 << (num - 8))
            if num in range(16, 24):
                value[0] &= ~(1 << (num - 16))
    #print(value)

    with SMBus(1) as bus:
        bus.write_i2c_block_data(0x20, 0, value)

#set enable PIN to HIGH
write_value("IO1_4", 1)
write_value("IO1_5", 1)

"""
reading rak5801 analog input via ads115 module 
"""
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
try:
	while True:
		total = 0
		for i in range(0,SAMPLE_NUM):
			# read rak5801 analog input 1
			value = adc.read_adc(ANALOG_INPUT_1, gain=GAIN)
			total += value
		raw = total / SAMPLE_NUM
		"""
		This is a number that ranges from -32768 to 32767 on the 16-bit ADS1115,
		A value of 0 means the signal is at a ground (reference) level, 32767  means 
		it's at or higher than the maximum voltage value for the current gain (4.096V by default),
		"""
		voltage = raw * 4.096 / 32767;
		#I=U/149.9(mA)
		current = voltage / 149.9 * 1000;  
		print("%.2f mA"%current)

except KeyboardInterrupt:
    logging.info('ctrl + c:')
    exit()
