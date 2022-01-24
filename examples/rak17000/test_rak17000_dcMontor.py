#!/usr/bin/env python3
"""
RAK17000 DC motor driver
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import time
from smbus2 import SMBus
import RPi.GPIO as GPIO


bus = SMBus(1)
write_value = [0xff, 0xff, 0xff]
bus.write_i2c_block_data(0x20, 0, write_value)


MOTOR_AIN1 = 23
MOTOR_AIN2 = 24

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(MOTOR_AIN1, GPIO.OUT)
GPIO.setup(MOTOR_AIN2, GPIO.OUT)

a1 = GPIO.PWM(MOTOR_AIN1, 50)
a2 = GPIO.PWM(MOTOR_AIN2, 50)
a1.start(0)
a2.start(0)
try:
	while True:
		
		for dc in range(0, 101, 5):
			a1.ChangeDutyCycle(dc)			
			time.sleep(0.1)

		time.sleep(0.2)
	
		for dc in range(100, -1, -5):
			a1.ChangeDutyCycle(dc)
			time.sleep(0.1)

		time.sleep(0.2)
		
		
		for dc in range(0, 101, 5):
			a2.ChangeDutyCycle(dc)
			time.sleep(0.1)

		time.sleep(0.2)

		for dc in range(100, -1, -5):
			a2.ChangeDutyCycle(dc)
			time.sleep(0.1)

		time.sleep(0.2)
		
except KeyboardInterrupt:
	pass
a1.stop()
a2.stop()
GPIO.cleanup()
