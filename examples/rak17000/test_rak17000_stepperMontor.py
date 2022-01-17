#!/usr/bin/env python3
"""
RAK17000 stepper motor driver
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import time
import RPi.GPIO as GPIO
from smbus2 import SMBus


MOTOR_AIN1 = 23
MOTOR_AIN2 = 24
MOTOR_BIN1 = 16 #gpio expender io2_2
MOTOR_BIN2 = 19


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(MOTOR_AIN1, GPIO.OUT)
GPIO.setup(MOTOR_AIN2, GPIO.OUT)
GPIO.setup(MOTOR_BIN2, GPIO.OUT)

bus = SMBus(1)

def set_bin1(value):

	if value == GPIO.HIGH:
		write_value = [0xff, 0xff, 0xff]
	else:
		write_value = [0x0, 0x0, 0x0]

	bus.write_i2c_block_data(0x20, 0, write_value)

def phaseA():
	GPIO.output(MOTOR_AIN1, GPIO.HIGH)
	GPIO.output(MOTOR_AIN2, GPIO.LOW)
	set_bin1(GPIO.LOW)
	GPIO.output(MOTOR_BIN2, GPIO.LOW)

def phaseB():
    GPIO.output(MOTOR_AIN1, GPIO.LOW)
    GPIO.output(MOTOR_AIN2, GPIO.HIGH)
    set_bin1(GPIO.LOW)
    GPIO.output(MOTOR_BIN2, GPIO.LOW)

def phaseC():
    GPIO.output(MOTOR_AIN1, GPIO.LOW)
    GPIO.output(MOTOR_AIN2, GPIO.LOW)
    set_bin1(GPIO.HIGH)
    GPIO.output(MOTOR_BIN2, GPIO.LOW)

def phaseD():
    GPIO.output(MOTOR_AIN1, GPIO.LOW)
    GPIO.output(MOTOR_AIN2, GPIO.LOW)
    set_bin1(GPIO.LOW)
    GPIO.output(MOTOR_BIN2, GPIO.HIGH)

try:
	while True:
		for i in range(0, 601):
			phaseA()
			time.sleep(0.007)
			phaseB()
			time.sleep(0.007)
			phaseC()
			time.sleep(0.007)
			phaseD()
			time.sleep(0.007)
		time.sleep(0.2)

		for i in range(0, 601):
			phaseD()
			time.sleep(0.007)
			phaseC()
			time.sleep(0.007)
			phaseB()
			time.sleep(0.007)
			phaseA()
			time.sleep(0.007)
		time.sleep(0.2)
				
except KeyboardInterrupt:
	pass
GPIO.cleanup()
