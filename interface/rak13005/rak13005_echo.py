#!/usr/bin/env python3
"""
Communication with a RAK13005 LINbus module
"""
__copyright__ = "Copyright 2021, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import sys
import time
import serial
from smbus2 import SMBus
import numpy
import gpiod

# RAK7301 WisBlock IO Slot#1: CHIP_NUM = 2, WK_PIN = 5, EN = 6
# RAK7391 WisBlock IO Slot#2: CHIP_NUM = 2, WK_PIN = 13, EN = 14
# RAK6421 IO Slot#1: CHIP_NUM = 0, WK_PIN = 6, EN = 12
# RAK6421 IO Slot#2: CHIP_NUM = 0, WK_PIN = 21, EN = 22
CHIP_NUM = 2
WK_PIN = 13
EN_PIN = 14

# RAK7301 WisBlock IO Slot#1: UART_PORT = "/dev/ttyUSB0"
# RAK7391 WisBlock IO Slot#2: UART_PORT = "/dev/ttyUSB1"
# RAK6421 both IO Slot#1 and SLot#2:  UART_PORT = "/dev/AMA0"
# Note: when you use RAK13005 in combination with RAK6421 Pi Hat,You should know
# there are two types of UART available on the Raspberry Pi - PL011 and mini UART.
# The PL011(/dev/ttyAMA0) is a capable, broadly 16550-compatible UART, while the mini UART(/dev/ttyS0)
# has a reduced feature set. mini UART is selected to be present on GPIO 14 (transmit) and 15 (receive) by default,
# however, mini UART can not have stable communication for RAK13005. You need to set PLO11 as your primary Uart.
# then you can set the UART_PORT to "/dev/ttyAMA0"
UART_PORT = "/dev/ttyUSB1"


class LinBus:
    def __init__(self, version, port, wkPin, enPin):
        self._version = version
        self._port = port
        self._wkPin = wkPin
        self._enPin = enPin
        self._ident = 0
        self._baudRate = 0
        self._serial = None

    def slave(self, baudRate, ident):
        self._baudRate = baudRate
        self._ident = ident
        self._serial = serial.Serial(self._port, self._baudRate, timeout=1)

    def protectID(self, ident):
        pid = ident & 0x3F
        tmp = (pid ^ (pid >> 1) ^ (pid >> 2) ^ (pid >> 4)) & 0x01
        pid |= tmp << 6
        tmp = ~((pid >> 1) ^ (pid >> 3) ^ (pid >> 4) ^ (pid >> 5)) & 0x01
        pid |= tmp << 7
        return pid

    def validateParity(self, ident):
        if ident == self.protectID(self._ident):
            return True
        else:
            return False

    def validateChecksum(self, data, size):
        chk = 0x00
        pid = self.protectID(self._ident)
        checksum = data[size-1]

        if not ((self._version == 1) or (pid == 0x3C) or (pid == 0x7D)):
            chk = pid
        for i in range(0, size-1):
            chk += data[i]
            if chk > 255:
                chk -= 255
        chk = 0xFF - chk

        if chk == checksum:
            return True
        else:
            return False

    def read(self, size):
        # check frame headr: break byte, sync byte and protected id byte.
        if self._serial.inWaiting() > 3:
            break_field = self._serial.read(1)
            if ord(break_field) != 0:
                return

            sync_field = self._serial.read(1)
            if ord(sync_field) != 0x55:
                return

            pid = self._serial.read(1)
            if not self.validateParity(ord(pid)):
                print("error:invalid data Parity")
                return
        else:
            return

        # read data and checksum, the last byte is checksum.
        if self._serial.inWaiting() > size+1:
            string = self._serial.read(size+1)
            data = numpy.frombuffer(string, dtype=numpy.uint8)
        else:
            print("no enough data!")
            return None

        if self.validateChecksum(data, size+1):
            print("recieve:", end="")
            for i in range(0, size):
                print("%d" % data[i], end=" ")
            print("")
        else:
            print("error: invalid data checksum")


if __name__ == '__main__':

    # set EN pin and WK pin to high
    chip = gpiod.chip(CHIP_NUM)
    en_line = chip.get_line(EN_PIN)
    wk_line = chip.get_line(WK_PIN)
    config = gpiod.line_request()
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    en_line.request(config)
    en_line.set_value(1)
    wk_line.request(config)
    wk_line.set_value(1)

    linbus = LinBus(1, UART_PORT, WK_PIN, EN_PIN)
    linbus.slave(9600, 1)

    while True:
        linbus.read(8)
        time.sleep(0.5)
