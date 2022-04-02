#!/usr/bin/env python3
"""
Read a gas concentration using rak12004.
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "0.1.0"
__status__ = "Production"



from mqx import mqx
import time
import RPi.GPIO as GPIO

'''
EN_PIN is enable pin for adc chip, must be pulled high before the reading
if you use IO slot#1, the GPIO pin Number is 12, slot#2 is 22
'''
EN_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.HIGH)
time.sleep(0.5)

mq2 = mqx.MQx()

mq2.config_cycle_time(mqx.CYCLE_TIME_32)
#in this example, we test ppm of smoke.
mq2.set_slope(mqx.MQ2_SMOKE_SLOPE)
mq2.set_intercept_y(mqx.MQ2_SMOKE_INTERCEPT_Y)

# we have calibrated Ro value in our envirenment.
mq2.set_Ro(mqx.MQ2_RO)

#you also can recalibrate Ro with method: calibrate_Ro
#sensor.calibrate_Ro(mqx.MQ2_RATIO_AIR)
try:
    while True:
        ppm = mq2.calibrate_ppm()
        print("ppm: {:.2f}".format(ppm))
        time.sleep(5)

except KeyboardInterrupt:
    None


