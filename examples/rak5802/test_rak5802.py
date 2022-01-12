#!/usr/bin/env python3
import serial
import time
import sys
import threading

PORT = "/dev/ttyUSB0" 

ser = serial.Serial(PORT,9600,timeout=1)
#print(ser.inWaiting())
while True:
	size = ser.inWaiting()
	data=ser.read(size).decode('utf-8')
	if len(data) > 0:
		print(data)
	time.sleep(1)

