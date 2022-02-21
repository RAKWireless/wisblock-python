#!/usr/bin/env python3
"""
RS485 serial communication using RAK5802 module
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import serial
import time

"""
RAK7391 WisBlock Slot #1: /dev/ttyUSB0
RAK7391 WisBlock Slot #2: /dev/ttyUSB1
"""
MODBUS_PORT = "/dev/ttyUSB1" 
MODBUS_BAUD = 9600

ser = serial.Serial(MODBUS_PORT, MODBUS_BAUD, timeout=1)

while True:
	size = ser.inWaiting()
	data=ser.read(size).decode('utf-8')
	if len(data) > 0:
		print(data)
	time.sleep(1)

