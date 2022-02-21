#!/usr/bin/env python3
"""
PI4IOE5V96224 GPIO Expander Example
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

from pi4ioesv96224.pi4ioesv96224 import GPIOExpander
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--read", action="append", nargs=2, type="int", dest="read", help="Reads the specified port (0 to 2) and pin (0 to 7)")
parser.add_option("-w", "--write", action="append", nargs=3, type="int", dest="write", help="Toggles the specified port (0 to 2) and pin (0 to 7)")
parser.add_option("--on", action="store_true", dest="allon", default=False, help="Sets everything ON")
parser.add_option("--off", action="store_true", dest="alloff", default=False, help="Sets everything OFF")
parser.add_option("--all", action="store_true", dest="readall", default=False, help="Reads and outputs current status")
(options, args) = parser.parse_args()

gpioe = GPIOExpander()

if options.read:
    for element in options.read:
        port = element[0]
        pin = element[1]
        value = gpioe.read(port, pin)
        print("IO%d_%d is %d" % (port, pin, value))

if options.write:
    for element in options.write:
        port = element[0]
        pin = element[1]
        value = element[2]
        gpioe.write(value, port, pin)
        print("IO%d_%d set to %d" % (port, pin, value))

if options.allon:
    gpioe.reset(0xFF)
    print("All pins set to 1")

if options.alloff:
    gpioe.reset(0x00)
    print("All pins set to 0")

if options.readall:
    values = gpioe.values
    for i in range (0, 3):
        print("Port %d is %s" % (i, format(values[i], "08b")))

