#!/usr/bin/env python3
"""
Communication with a RAK13005 LINbus module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import sys
import time
import serial
from smbus2 import SMBus
import numpy

I2C_ADDR    = 0x20
I2C_BUS     = 1
IO2_4 = 20
IO2_6 = 22
WK = IO2_4
EN = IO2_6


class LinBus:
	def __init__(self, version, port, wkPin, enPin, txPin):
		self._version = version
		self._port = port
		self._wkPin = wkPin
		self._enPin = enPin
		self._txPin = txPin
		self._ident = 0;
		self._baudRate = 0
		self._baudRateTmp = 0
		self._serial = None
		self._gHead1 = 0x55
		self._gHead2 = 0
	def slave(self, baudRate, ident):
		self._baudRate = baudRate
		self._ident = ident
		self._serial = serial.Serial(self._port, self._baudRate, timeout=1)
		self._baudRateTmp = 0.692 * baudRate

	def protectID(self, ident):
		pid = ident & 0x3F
		tmp = (pid ^ (pid>>1) ^ (pid>>2) ^ (pid>>4)) & 0x01
		pid |= tmp << 6
		tmp = ~((pid>>1) ^ (pid>>3) ^ (pid>>4) ^ (pid>>5)) & 0x01
		pid |= tmp << 7
		return pid

	def validateParity(self, ident):
		if self._ident == self.protectID(ident):
			return True
		else:
			return False				

	def validateChecksum(self, data, size):
		chk = 0x00
		pid = self.protectID(data[1])	
		checksum = data[size-1]
			 
		if not ((self._version == 1) or (pid == 0x3C) or (pid == 0x7D)):
			chk = pid
		for i in range(2, size):
			chk += data[i]
			if chk > 255:
				chk -= 255
		chk = 0xFF - chk

		if chk == checksum:
			return True
		else:
			return False
	
	def read(self, size):
		if self._serial.inWaiting() > (size+3):
			self._gHead2 = self._gHead1
			string = self._serial.read(size+3)
			data =  numpy.fromstring(string, dtype=numpy.uint8)
			for i in range(0, size+3):
				print("%d" % data[i],end=" ")
			print("")
		else:
			print("no data!")
			return None			
			
		if self._gHead2 != 0x55:
			return None
		
		if not self.validateParity(data[0]):
			print("invalid data Parity")
			return None
		 
		if self.validateChecksum(data, size+3):					
			for i in range(0, size):
				print("%d" % data[i+2],end=" ")
			print("")
		else:
			print("invalid data checksum")

if __name__ == '__main__' :

	#set EN pin and WK pin to high 
	bus = SMBus(I2C_BUS)
	write_value = [0xff, 0xff, 0xff]
	bus.write_i2c_block_data(I2C_ADDR, 0, write_value)
	
	
	linbus = LinBus(1, "/dev/ttyUSB0", WK, EN, 0)
	linbus.slave(9600, 1)

	while True:
		linbus.read(8)
		time.sleep(1)
