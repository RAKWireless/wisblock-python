#!/usr/bin/env python3
"""
Toggle led from gpio expander TPT29555 on rak7391.
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

from PCA95XX import PCA95XX_GPIO
import time

# Assumes a PCA9555 with 16 GPIO's
bus = 1
# I2C address of the GPIO expander, can be 0x23 or 0x27 on RAK7391
address = 0x27
pinnum = 16
pin = 7

chip = PCA95XX_GPIO(bus, address, pinnum) 
# 0 is output
chip.setup(pin, 0);
while True:
    chip.output(pin, 0);
    time.sleep(1);
    chip.output(pin, 1);
    time.sleep(1);
