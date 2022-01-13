#!/usr/bin/env python3
"""
RS485 communication using RAK5802 module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import serial
import time
import sys

"""
rak5802 module converts the RS485 signals into UART signals.
"""

"""
/dev/ttyUSB0 <---> wisblock1
/dev/ttyUSB1 <---> wisblock2
"""
PORT = "/dev/ttyUSB0" 

ser = serial.Serial(PORT,9600,timeout=1)

while True:
	size = ser.inWaiting()
	data=ser.read(size).decode('utf-8')
	if len(data) > 0:
		print(data)
	time.sleep(1)

