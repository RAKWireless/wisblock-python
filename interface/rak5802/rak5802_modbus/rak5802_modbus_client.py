#!/usr/bin/env python3
"""
Simple ModBUS RTU sync client based on a RAK5802
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

"""
RAK7391 WisBlock Slot #1: /dev/ttyUSB0
RAK7391 WisBlock Slot #2: /dev/ttyUSB1
"""
MODBUS_PORT = "/dev/ttyUSB0" 
MODBUS_BAUD = 9600
DEVICE_ID = 42

def run_sync_client():
    
    # Connect to device
    client = ModbusClient(method='rtu', port=MODBUS_PORT, timeout=1, baudrate=MODBUS_BAUD)
    client.connect()

    # Loop
    while True:

        # Toggle coil at address 0x00
        response = client.read_coils(0x00, 1, unit=DEVICE_ID)
        value = 1 - response.bits[0]
        print("Turning LED %s" % ("ON" if value else "OFF"))
        client.write_coil(0x00, value, unit=DEVICE_ID)

        # Read sensor (2 registers at address 0x00)
        response = client.read_holding_registers(0x00, 2, unit=DEVICE_ID)
        (humidity, temperature) = response.registers
        print("Humidity: %d%%\nTemperature %.2fC" % (humidity, temperature/100.0))

        # Delay 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    run_sync_client()    