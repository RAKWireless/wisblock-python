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
import json

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

#set enable pin to HIGH
write_value("IO2_6", 1)
write_value("IO2_7", 1)

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
