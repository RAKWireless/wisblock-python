#!/usr/bin/env python3
"""
Turns on and off the relay in the RAK13007
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
from pi4ioesv96224.pi4ioesv96224 import GPIOExpander

HIGH = 1
LOW  = 0

#the relay pin connect to IO2_2 when use wisblock slot#1
#if you want use slot#2, please change PIN valuse to 3(IO2_3)
PORT = 2
PIN  = 2

gpioe = GPIOExpander()

def run_toggle():
	#Loop
	while True:
		#Set relay pin to low
		gpioe.write(LOW, PORT, PIN)
		time.sleep(1)
		#Set relay pin to high
		gpioe.write(HIGH, PORT, PIN)
		time.sleep(1)

if __name__ == "__main__":
	run_toggle()
			


