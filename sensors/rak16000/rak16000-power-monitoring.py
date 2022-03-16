#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
import time

# RAK16000 has a 100 mΩ (0.1 Ω) shunt resistor placed between the power supply and the load
SHUNT_OHMS = 0.1


def read():
    # The default 7-bit I2C address is 0x41
    ina = INA219(SHUNT_OHMS, address=0x41)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f W" % (ina.power()/1000))
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
        print()
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    while True:
        read()
        # outputs to the console every 5 seconds
        time.sleep(5)
