#!/usr/bin/env python3
"""
Read pressure and temperature data with RAK1902(LPS22HB).
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
import board
import adafruit_lps2x

# Default I2C address is 0x5D, but for RAK1902，it is set to 0x5C
_LPS2X_ADDRESS = 0x5C
i2c = board.I2C()
lps = adafruit_lps2x.LPS22(i2c, _LPS2X_ADDRESS)

while True:
    print("Pressure: %.2f hPa" % lps.pressure)
    print("Temperature: %.2f C" % lps.temperature)
    time.sleep(1)
