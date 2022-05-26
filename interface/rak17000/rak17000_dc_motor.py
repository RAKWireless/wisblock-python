#!/usr/bin/env python3
"""
RAK17000 DC motor driver
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import time
import RPi.GPIO as GPIO
import gpiod

#RAK7391, IO Slot#1: NSLEEP = 6, AIN1 = 11, AIN2 = 8
#RAK7391, IO Slot#2: NSLEEP = 14, AIN1 = 11, AIN2 = 7
NSLEEP = 14
AIN1 = 11
AIN2 = 7

# set nsleep pin to High
chip = gpiod.chip(2)
nsleep = chip.get_line(NSLEEP)
config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
nsleep.request(config)
nsleep.set_value(1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

a1 = GPIO.PWM(AIN1, 50)
a2 = GPIO.PWM(AIN2, 50)

a1.start(0)
a2.start(0)

try:
    while True:
        GPIO.output(AIN2, GPIO.LOW)
        time.sleep(0.5)

        for dc in range(0, 101, 1):
            a1.ChangeDutyCycle(dc)
            time.sleep(0.02)
        time.sleep(0.5)

        for dc in range(100, -1, -1):
            a1.ChangeDutyCycle(dc)
            time.sleep(0.02)
        time.sleep(0.5)

        GPIO.output(AIN1, GPIO.LOW)
        time.sleep(0.5)

        for dc in range(0, 101, 1):
            a2.ChangeDutyCycle(dc)
            time.sleep(0.02)
        time.sleep(0.5)

        for dc in range(100, -1, -1):
            a2.ChangeDutyCycle(dc)
            time.sleep(0.02)
        time.sleep(0.5)

except KeyboardInterrupt:
    pass

a1.stop()
a2.stop()
GPIO.cleanup()
