#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
identify a fingerprint
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
import gpiod
from datetime import timedelta
import time

## set interrput pin
OUT_PIN = 6 
chip = gpiod.chip(0)
out_line = chip.get_line(OUT_PIN)
config = gpiod.line_request()
config.request_type = gpiod.line_request.EVENT_BOTH_EDGES
out_line.request(config)

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

print('Waiting for finger...')
print('You can click ctrl+c to exit process.\n')

try:
    while True:
        if out_line.event_wait(timedelta(seconds=1)):
            event = out_line.event_read()
            if event.event_type == gpiod.line_event.FALLING_EDGE:
                time.sleep(0.1)
                if out_line.get_value() == 0:
                    print("Finger detected!")
                    try:
                        # Waiting for the finger and validate it
                        while ( f.readImage() == False ):
                                pass

                        ## Converts read image to characteristics and stores it in charbuffer 1
                        f.convertImage(FINGERPRINT_CHARBUFFER1)

                        ## Searchs template
                        result = f.searchTemplate()

                        positionNumber = result[0]
                        accuracyScore = result[1]

                        if ( positionNumber == -1 ):
                            print('No match found!\n')
                        else:
                            print('Found template at position #' + str(positionNumber))
                            print('The accuracy score is: ' + str(accuracyScore)) 
                            print()
                    except Exception as e:
                        print('Operation failed!')
                        print('Exception message: ' + str(e))
                        print()
except KeyboardInterrupt:
    exit()

