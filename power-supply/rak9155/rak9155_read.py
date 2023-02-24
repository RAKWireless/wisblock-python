#!/usr/bin/python3 

import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


MODBUS_BAND=9600
MODBUS_PORT="/dev/ttyUSB0"

DEVICE_ID=0x6e

# Register address table

BATTERY_VOLTAGE = 0x6000
REMAINING_CAP  = 0x6005
FULL_CHARGE_CAP = 0x6006
BATTERY_STATUS	= 0x600e
BATTERY_MODE	= 0x600f

client = ModbusClient(method="rtu", port=MODBUS_PORT, timeout=1, baudrate=MODBUS_BAND)

while True:

    # Read volatge value
    response = client.read_holding_registers(BATTERY_VOLTAGE, 1, unit=DEVICE_ID)
    voltage = response.registers[0] * 0.01

    # Read battery work mode
    response = client.read_holding_registers(BATTERY_MODE, 1, unit=DEVICE_ID)
    if response.registers[0] == 2:
        mode = "discharge"
    if response.registers[0] == 3:
        mode = "charge"
    if response.registers[0] == 5:
        mode = "full charged"
    if response.registers[0] == 6:
        mode = "epmty"

    # Read percentage of battery remaining
    remaining = client.read_holding_registers(REMAINING_CAP, 1, unit=DEVICE_ID)
    full = client.read_holding_registers(FULL_CHARGE_CAP, 1, unit=DEVICE_ID)
    percentage = remaining.registers[0] / full.registers[0] * 100

    print("voltage: %.2fv" % voltage)
    print("mode: %s" % mode)
    print("remaining: %d%%" % percentage)
    print("")

    time.sleep(1)
