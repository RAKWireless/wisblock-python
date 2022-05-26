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
import gpiod

# RAK7391 IO Slot#1: NSLEEP = 6, AIN1 = 11, AIN2 = 8, BIN1 = 3, BIN2 = 10
# RAK7391 IO Slot#2: NSLEEP = 14, AIN1 = 11, AIN2 = 7, BIN1 = 11, BIN2 = 10
NSLEEP = 14
AIN1 = 11
AIN2 = 7
BIN1 = 11
BIN2 = 10

# set nsleep pin to High
chip = gpiod.chip(2)
nsleep = chip.get_line(NSLEEP)
config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
nsleep.request(config)
nsleep.set_value(1)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

bin1 = chip.get_line(BIN1)
bin1.request(config)


def phaseA():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    bin1.set_value(0)
    GPIO.output(BIN2, GPIO.LOW)


def phaseB():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    bin1.set_value(0)
    GPIO.output(BIN2, GPIO.LOW)


def phaseC():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    bin1.set_value(1)
    GPIO.output(BIN2, GPIO.LOW)


def phaseD():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    bin1.set_value(0)
    GPIO.output(BIN2, GPIO.HIGH)

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
