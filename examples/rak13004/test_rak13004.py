#!/usr/bin/env python3
"""
Breathing LED using RAK13004 PWM module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import time
import Adafruit_PCA9685	

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
	for i in range(0, 4096):
		pwm.set_pwm(0, 0, i)

	for i in range(0, 4096):
		pwm.set_pwm(0, 0, 4095-i)

