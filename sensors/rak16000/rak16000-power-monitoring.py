#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
import time

SHUNT_OHMS = 0.1


def read():
    ina = INA219(SHUNT_OHMS, address=0x41)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
        print()
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    while True:
        read()
        time.sleep(5)
