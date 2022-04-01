# Author: rakwireless.com
# Version：0.0.1
# License: MIT

"""
This example shows connecting to the PN532 with I2C
"""

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import time
import datetime

print("""
nfc_read.py - read uid of RAK13600(PN532).
Press Ctrl+C to exit!
""")

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

# harware reset
reset_pin = DigitalInOut(board.D6)
# wakeup! this means we don't need to do the I2C clock-stretch thing
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")

name_list = {'bcf024b5': 'Mr Brown', 'dcaffd02': 'Mrs Blair'}

detected_device_list = {}

try:
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is None:
            continue
        
        strId = ''.join([hex(i)[2:].rjust(2, '0') for i in uid])
        if detected_device_list.__contains__(strId):
            if int(time.time()) - detected_device_list[strId] < 5:
                time.sleep(0.2)
                continue

        detected_device_list[strId] = int(time.time())
        
        if name_list.__contains__(strId):
            print(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Hello,',
                name_list[strId],
                '!'
            )
        else:
            print(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Unregistered card !'
            )

        time.sleep(0.2)
except KeyboardInterrupt:
    pass
