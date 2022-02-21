#!/usr/bin/env python3
"""
PI4IOE5V96224 GPIO Expander Helper Library
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

from smbus2 import SMBus
from optparse import OptionParser

GPIOE_PORTS = [
    "IO0_7", "IO0_6", "IO0_5", "IO0_4", "IO0_3", "IO0_2", "IO0_1", "IO0_0",
    "IO1_7", "IO1_6", "IO1_5", "IO1_4", "IO1_3", "IO1_2", "IO1_1", "IO1_0",
    "IO2_7", "IO2_6", "IO2_5", "IO2_4", "IO2_3", "IO2_2", "IO2_1", "IO2_0",
]
GPIOE_BUS = 1
GPIOE_ADDRESS = 0x20

class gpioe:

    address = 0x20
    values = []

    def __init__(self, bus=GPIOE_BUS, address=GPIOE_ADDRESS, ** kwargs):
        self.bus = bus
        self.address = address
        with SMBus(self.bus) as bus:
            self.values = bus.read_i2c_block_data(self.address, 0, 3)

    def debug(self):
        for i in range (0, 3):
            print("Port %d is %s" % (i, format(self.values[i], "08b")))


    def get_port_pin(self, port):
        try:
            index = GPIOE_PORTS.index(port)
            port = int(index / 8)
            pin = index % 8
            return (port, pin)
        except ValueError:
            raise Exception("Wrong port identifier: " + port)

    def read(self, port, pin):

        #(port, pin) = self.get_port_pin(port)

        with SMBus(self.bus) as bus:
            self.values = bus.read_i2c_block_data(self.address, 0, 3)

        return (self.values[port] >> pin) & 0x01

    def reset(self, value):
   
        with SMBus(self.bus) as bus:
            bus.write_i2c_block_data(self.address, 0, [value, value, value])

    def write(self, port, pin, value):

        #(port, pin) = self.get_port_pin(port)
        
        with SMBus(self.bus) as bus:

            self.values = bus.read_i2c_block_data(self.address, 0, 3)
            print("Current:")
            self.debug()

            if value:
                self.values[port] |= (1 << pin)
            else:
                self.values[port] &= ~(1 << pin)
        
            print("Intent:")
            self.debug()

            # rotate element
            #mask = self.values[2:] + self.values[:2]
            mask = self.values
            bus.write_i2c_block_data(self.address, 0, mask)
            
            self.values = bus.read_i2c_block_data(self.address, 0, 3)
            print("Finally:")
            self.debug()
        

if __name__ == "__main__":

    parser = OptionParser('./test_GPIO_expander.py -r <GPIO to read> -w <GPIO to write><value to write>')
    parser.add_option("-r", "--read", type="string", action="append", nargs=2, dest="read", help="Reads the specified port (port must be a valid port name such as IO1_3, IO2_4)")
    parser.add_option("-w", "--write", type="string", action="append", nargs=3, dest="write", help="Toggles the specified port (port must be a valid port name such as IO1_3, IO2_4, value must be 0 or 1)")
    parser.add_option("--all-on", action="store_true", dest="allon", default=False, help="Sets everything ON")
    parser.add_option("--all-off", action="store_true", dest="alloff", default=False, help="Sets everything OFF")
    parser.add_option("--all", action="store_true", dest="all", default=False, help="Reads and outputs all values")
    (options, args) = parser.parse_args()

    gpioe = gpioe(1, 0x20)

    if options.read:
        port = int(options.read[0][0])
        pin = int(options.read[0][1])
        value = gpioe.read(port, pin)
        print("IO%d_%d is %d" % (port, pin, value))

    if options.write:
        port = int(options.write[0][0])
        pin = int(options.write[0][1])
        value = int(options.write[0][2])
        gpioe.write(port, pin, value)
        print("IO%d_%d set to %d" % (port, pin, value))

    if options.allon:
        gpioe.reset(0xFF)

    if options.alloff:
        gpioe.reset(0x00)

    if options.all:
        values = gpioe.values
        for i in range (0, 3):
            print("Port %d is %s" % (i, format(values[i], "08b")))

