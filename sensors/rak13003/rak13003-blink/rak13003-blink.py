#!/usr/bin/env python3
"""
Blinks an LED at 1Hz for 5 seconds, using the RAK13003 module
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import RPi.GPIO as GPIO

# When mount RAK13003/14003 on slot 1 on RAK6421, reset pin is gpio 16
# (board pin 36) on RaspberryPi's 40-pin header
reset_pin = 16
# When mount RAK13003/14003 on slot 1 on RAK6421, reset pin is gpio 24
# (board pin 18) on RaspberryPi's 40-pin header
# reset_pin = 24

# Reset device first
GPIO.setup(reset_pin, GPIO.OUT)
GPIO.output(reset_pin, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(reset_pin, GPIO.LOW)
time.sleep(0.1)
GPIO.output(reset_pin, GPIO.HIGH)
time.sleep(0.1)

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of the MCP23017 class depending on
# which chip you're using:
# mcp = MCP23017(i2c)  # MCP23017

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
mcp = MCP23017(i2c, address=0x24, reset=True)

# Now call the get_pin function to get an instance of a pin on the chip.
# This instance will act just like a digitalio.DigitalInOut class instance
# and has all the same properties and methods (except you can't set pull-down
# resistors, only pull-up!).
# For the MCP23017 you specify a pin number from
# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
# Take pin 0 as an example
pin = mcp.get_pin(0)

# Setup pin0 as an output that's at a high logic level.
pin.switch_to_output(value=True)

# Blink pin 0 on and then off for 5 seconds with a frequency of 1 Hz.
for i in range(0, 5):
    pin.value = True
    time.sleep(0.5)
    pin.value = False
    time.sleep(0.5)
    i += 1

# Reset to all inputs with no pull-ups and no inverted polarity.
# Comment out the following line if you don't want to reset.
mcp = MCP23017(i2c, address=0x24, reset=True)
