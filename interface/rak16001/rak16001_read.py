#!/usr/bin/env python3
"""
Reads values from a analog input using the RAK16001 module
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import smbus2 as smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# The address of ADS7830 can be changed making the option of connecting multiple devices
# address=0x48    # 0x48, 1001 000
# address=0x49    # 0x49, 1001 001
address=0x4A    # 0x4A, 1001 010
# address=0x4B    # 0x4B, 1001 011

# The command byte determines ADS7830's operating mode,
# check https://www.ti.com/lit/ds/symlink/ads7830.pdf table 1 and table 2 for more details.
# The command byte have 3 parts: Single-Ended/Differential Inputs, Channel Selections, and Power-Down

# 1. SD: Single-Ended/Differential Inputs (Table 2)
# sd = '0'  # Differential Inputs
sd = '1'  # Single-Ended Inputs

# 2. C2 - C0: Channel Selections (Table 2)
channel = '000'  # Single-Ended, Channel 0
# channel = '001'  # Single-Ended, Channel 1
# channel = '010'  # Single-Ended, Channel 2
# channel = '011'  # Single-Ended, Channel 3
# channel = '100'  # Single-Ended, Channel 4
# channel = '101'  # Single-Ended, Channel 5
# channel = '110'  # Single-Ended, Channel 6
# channel = '111'  # Single-Ended, Channel 7

# 3. PD1-0: Power-Down Selection (Table 1)
# pd = '00'  # Power Down Between A/D Converter Conversions
pd = '01'  # Internal Reference OFF and A/D Converter ON
# pd = '10'  # Internal Reference ON and A/D Converter OFF
# pd = '11'  # Internal Reference ON and A/D Converter ON

# Build the command byte
command_byte = int(sd + channel + pd + '00', 2)

# Reference voltage
ref_vol = 3.3

try:
    while True:
        
        # Send command to read one byte from given channel
        bus.write_byte(address, command_byte)
        time.sleep(0.5)
        raw_data = bus.read_byte(address)

        # Transform into actual voltage
        measurement = raw_data * ref_vol / 255
        
        # Output data to screen
        print("Digital value of analog input : %.2f V" % measurement)
        
        # Do this every second
        time.sleep(1)

except KeyboardInterrupt:
    print("Keyboard interrupt, exit")
    exit()
