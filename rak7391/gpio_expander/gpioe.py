#!/usr/bin/env python3
"""
PI4IOE5V96224 GPIO Expander Helper Library
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

from smbus2 import SMBus, i2c_msg
from optparse import OptionParser

GPIOE_BUS = 1
GPIOE_ADDRESS = 0x20

class gpioe:

    address = 0x20
    values = [0, 0, 0]

    def __init__(self, bus=GPIOE_BUS, address=GPIOE_ADDRESS, **kwargs):
        self.bus = SMBus(bus)
        self.address = address
        msg = i2c_msg.read(self.address, 3)
        self.bus.i2c_rdwr(msg)
        self.values = list(msg)

    def reset(self, value):
        msg = i2c_msg.write(self.address, [value, value, value])
        self.bus.i2c_rdwr(msg)

    def read(self, port, pin):
        msg = i2c_msg.read(self.address, 3)
        self.bus.i2c_rdwr(msg)
        self.values = list(msg)
        return (self.values[port] >> pin) & 0x01

    def write(self, value, port, pin=0):
        msg = i2c_msg.read(self.address, 3)
        self.bus.i2c_rdwr(msg)
        self.values = list(msg)
        if value:
            self.values[port] |= (1 << pin)
        else:
            self.values[port] &= ~(1 << pin)
        msg = i2c_msg.write(self.address, self.values)
        self.bus.i2c_rdwr(msg)
        

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-r", "--read", type="string", action="append", nargs=2, dest="read", help="Reads the specified port (0 to 2) and pin (0 to 7)")
    parser.add_option("-w", "--write", type="string", action="append", nargs=3, dest="write", help="Toggles the specified port (0 to 2) and pin (0 to 7)")
    parser.add_option("--on", action="store_true", dest="allon", default=False, help="Sets everything ON")
    parser.add_option("--off", action="store_true", dest="alloff", default=False, help="Sets everything OFF")
    parser.add_option("--all", action="store_true", dest="all", default=False, help="Reads and outputs current status")
    (options, args) = parser.parse_args()

    gpioe = gpioe()

    if options.read:
        port = int(options.read[0][0])
        pin = int(options.read[0][1])
        value = gpioe.read(port, pin)
        print("IO%d_%d is %d" % (port, pin, value))

    if options.write:
        port = int(options.write[0][0])
        pin = int(options.write[0][1])
        value = int(options.write[0][2])
        gpioe.write(value, port, pin)
        print("IO%d_%d set to %d" % (port, pin, value))

    if options.allon:
        gpioe.reset(0xFF)

    if options.alloff:
        gpioe.reset(0x00)

    if options.all:
        values = gpioe.values
        for i in range (0, 3):
            print("Port %d is %s" % (i, format(values[i], "08b")))

