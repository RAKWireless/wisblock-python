#!/usr/bin/env python3
"""
Read a gas concentration using rak12009.
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "0.1.0"
__status__ = "Production"

import time
import RPi.GPIO as GPIO
import math
from adc121c021 import ADC121C021, CYCLE_TIME_32

I2C_BUS = 0x1
I2C_ADDRESS = 0x55
VOLTAGE_REF = 5
RL = 10
RO = 16.1
RATIO_AIR = 1
ALCOHOL_SLOPE = -0.888
ALCOHOL_INTERCEPT_Y = 0.738

# EN_PIN is Power enable pin (active high)
# RAK6421 IO Slot#1: EN_PIN = 12
# RAK6421 IO Slot#2: EN_PIN = 22

EN_PIN = 12


def calibrate_Ro(adc, ratio_air):
    total = 0
    for i in range(100):
        total += adc.read_adc_voltage()
        volt = total / 100
    Rs_air = VOLTAGE_REF * RL / volt - RL
    Ro = Rs_air / ratio_air
    return Ro


def calculate_ppm(adc, Ro, intercept_y, slope):
    volt = adc.read_adc_voltage()
    Rs = VOLTAGE_REF * RL / volt - RL
    ratio = Rs / Ro
    ppm_log10 = (math.log10(ratio) - intercept_y) / slope
    ppm = math.pow(10, ppm_log10)
    return ppm

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.HIGH)
time.sleep(0.5)

adc = ADC121C021(bus=I2C_BUS, addr=I2C_ADDRESS)
adc.config_cycle_time(CYCLE_TIME_32)
ro = calibrate_Ro(adc, RATIO_AIR)

try:
    while True:
        ppm = calculate_ppm(adc, ro, ALCOHOL_INTERCEPT_Y, ALCOHOL_SLOPE)
        print("ppm:{:.2f}".format(ppm))
        time.sleep(5)
except KeyboardInterrupt:
    None


