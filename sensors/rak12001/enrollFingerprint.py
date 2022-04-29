#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enroll new finger
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
import gpiod
from datetime import timedelta

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

print('You can Click ctrl+c to exit process')

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
print('Waiting for finger...')
## Tries to enroll new finger
try:
    while True:
        if out_line.event_wait(timedelta(seconds=1)):
            event = out_line.event_read()
            if event.event_type == gpiod.line_event.FALLING_EDGE:
                time.sleep(0.1)
                if out_line.get_value() == 0:
                    try:
                        # Waiting for the finger and validate it
                        while ( f.readImage() == False ):
                                pass

                        ## Converts read image to characteristics and stores it in charbuffer 1
                        f.convertImage(FINGERPRINT_CHARBUFFER1)

                        ## Searchs template
                        result = f.searchTemplate()
                        positionNumber = result[0]
                        if ( positionNumber >= 0 ):
                            print('Template already exists at position #' + str(positionNumber))
                            print('Please enroll another finger !\n')
                        else:
                            print('Please move out your finger from sensor.\n')
                            while out_line.get_value() == 0:
                                time.sleep(1)
                                
                            print('Waiting for the same finger again...\n')
                            while out_line.get_value() == 1:
                                time.sleep(1)

                            ## Wait that finger is read again
                            while ( f.readImage() == False ):
                                pass

                            ## Converts read image to characteristics and stores it in charbuffer 2
                            f.convertImage(FINGERPRINT_CHARBUFFER2)

                            ## Compares the charbuffers
                            if ( f.compareCharacteristics() == 0 ):
                                print('Fingers do not match, please enroll again.\n')

                            ## Creates a template
                            f.createTemplate()

                            ## Saves template at new position number
                            positionNumber = f.storeTemplate()
                            print('Finger enrolled successfully!')
                            print('New template position #' + str(positionNumber))
                            while out_line.get_value() == 0:
                                print('Please move out your finger from sensor.')
                                time.sleep(2)
                            print('\nEnroll another finger or click ctrl+c to exit.\n')
                        
                    except Exception as e:
                        print('Operation failed!')
                        print('Exception message: ' + str(e))

except KeyboardInterrupt:
    exit()
