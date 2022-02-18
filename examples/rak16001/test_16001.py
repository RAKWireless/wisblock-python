#!/usr/bin/env python3
"""
Reads values from a 4-20mA sensor using a RAK5801 module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

# Distributed with a free-will license. Use it any way you want, profit or free, provided it fits in the licenses of
# its associated works. ADS7830 This code is designed to config ADS7830 ADC device and handle the data, ADS7830 is
# available from ControlEverything.com. https://www.controleverything.com/content/Analog-Digital-Converters?sku
# =ADS7830_I2CADC

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# Send command byte
#               0x04(04)        Differential inputs, Channel-0, Channel-1 selected
# The address of ADS7830 can be changed making the option of connecting multiple devices
# address=0x48    # 0x48, 1001 000 (ADDR = GND)
# address=0x49    #0x49, 1001 001 (ADDR = VDD)
address = 0x4a  # 0x4A, 1001 010 (ADDR = SDA)
# address=0x4b    # 0x4B, 1001 011 (ADDR = SCL)

# The command byte determines ADS7830's operating mode, check https://www.ti.com/lit/ds/symlink/ads7830.pdf table 1
# and table 2 for more details.
# The command byte have 3 parts: Single-Ended/Differential Inputs, Channel Selections, and Power-Down
# 1. SD: Single-Ended/Differential Inputs
# sd = '0'  # Differential Inputs
sd = '1'  # Single-Ended Inputs

# 2. C2 - C0: Channel Selections
channel = '000'  # Single-Ended, Channel 0
# channel = '001'  # Single-Ended, Channel 1
# channel = '010'  # Single-Ended, Channel 2
# channel = '011'  # Single-Ended, Channel 3
# channel = '100'  # Single-Ended, Channel 4
# channel = '101'  # Single-Ended, Channel 5
# channel = '110'  # Single-Ended, Channel 6
# channel = '111'  # Single-Ended, Channel 7

# 3. PD1: Power-Down Selection
# pd = '00'  # Power Down Between A/D Converter Conversions
pd = '01'  # Internal Reference OFF and A/D Converter ON
# pd = '10'  # Internal Reference ON and A/D Converter OFF
# pd = '11'  # Internal Reference ON and A/D Converter ON


command_byte = hex(int((sd + channel + pd + '00'), 2))
try:
    while True:
        bus.write_byte(address, int(command_byte, 16))
        time.sleep(0.5)
        # Read data back, 1 byte
        raw_data = bus.read_byte(address)
        # reference voltage is 3 Volts
        measurement = raw_data * 3 / 255
        # Output data to screen
        print("Digital value of analog input : %.2f V" % measurement)
        time.sleep(1)
except KeyboardInterrupt:
    print("Keyboard interrupt, exit")
    exit()
