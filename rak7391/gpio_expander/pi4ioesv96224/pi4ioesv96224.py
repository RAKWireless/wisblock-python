#!/usr/bin/env python3
"""
PI4IOE5V96224 GPIO Expander Library
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "0.1.0"
__status__ = "Production"

from smbus2 import SMBus, i2c_msg

GPIOE_BUS = 1
GPIOE_ADDRESS = 0x20
GPIOE_LAZY = False

class GPIOExpander:

    address = GPIOE_ADDRESS
    lazy = GPIOE_LAZY
    values = [0, 0, 0]

    def __init__(self, bus=GPIOE_BUS, address=GPIOE_ADDRESS, lazy=GPIOE_LAZY, **kwargs):
        self.bus = SMBus(bus)
        self.address = address
        self.lazy = lazy
        self.sync()

    def reset(self, value):
        self.values = [value, value, value]
        msg = i2c_msg.write(self.address, self.values)
        self.bus.i2c_rdwr(msg)

    def sync(self):
        msg = i2c_msg.read(self.address, 3)
        self.bus.i2c_rdwr(msg)
        self.values = list(msg)

    def read(self, port, pin):
        if not self.lazy:
            self.sync()
        return (self.values[port] >> pin) & 0x01

    def write(self, value, port, pin):
        if not self.lazy:
            self.sync()
        if value:
            self.values[port] |= (1 << pin)
        else:
            self.values[port] &= ~(1 << pin)
        msg = i2c_msg.write(self.address, self.values)
        self.bus.i2c_rdwr(msg)
        