#!/usr/bin/env python3
"""
Breathing LED using RAK13004 PWM module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import time
from smbus2 import SMBus
import Adafruit_PCA9685	
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

#active LOW output enable for PCA9685 OE PIN
write_value("IO1_6", 0)
write_value("IO1_7", 0)



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
	for i in range(0, 4096, 10):
		pwm.set_pwm(0, 0, i)

	for i in range(0, 4096, 10):
		pwm.set_pwm(0, 0, 4095-i)

