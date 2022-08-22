#!/usr/bin/env python3
"""
Breathing LED using RAK13004 PWM module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import gpiod
import Adafruit_PCA9685	

#RAK7391 WisBlock IO Slot#1: CHIP_NUM = 3, OE_PIN = 6
#RAK7391 WisBlock IO Slot#2: CHIP_NUM = 3, OE_PIN = 14
#RAK6421 IO Slot#1: CHIP_NUM = 0, OE_PIN = 12
#RAK6421 IO Slot#2: CHIP_NUM = 0, OE_PIN = 22

CHIP_NUM = 3
OE_PIN = 6

#active LOW output enable for PCA9685 OE PIN
chip = gpiod.chip(CHIP_NUM)
line = chip.get_line(OE_PIN)
config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
line.request(config)
line.set_value(0)


# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
# Set frequency to 60hz
pwm.set_pwm_freq(60)


# breathing light using LED on Channel 0 of the PCA9685
# Wire up the LED  on  Channel 0 such that 
#    Shortleg of LED goes to GND and
#    Long leg goes to PWM pin on channel 0

while True:
	for i in range(0, 4096, 5):
		pwm.set_pwm(0, 0, i)

	for i in range(0, 4096, 5):
		pwm.set_pwm(0, 0, 4095-i)
