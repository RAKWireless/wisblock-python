#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deletes a fingerprint from sensor
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

from pyfingerprint.pyfingerprint import PyFingerprint
import time

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

print('You can click ctrl+c to exit process.\n')

## Tries to delete the template of the finger
try:
    while True:
        try:
            count = f.getTemplateCount()
            print('Currently used templates: ' + str(count) +'/'+ str(f.getStorageCapacity()))
            if count == 0:
                print('Fingerprint is empty, no need to delete!')
                exit(0)

            positionNumber = input('Please enter the template position you want to delete: ')
            positionNumber = int(positionNumber)

            if f.deleteTemplate(positionNumber) == True:
                print('Template deleted!\n')
                time.sleep(1);

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            print()
except KeyboardInterrupt:
    exit()