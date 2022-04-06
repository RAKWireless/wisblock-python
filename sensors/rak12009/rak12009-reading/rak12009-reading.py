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
if you use IO slot#1 of RAK6421, the GPIO pin Number is 12, slot#2 is 22
'''
EN_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.HIGH)
time.sleep(0.5)

mq3 = mqx.MQx(bus=mqx.I2C_BUS, addr=mqx.I2C_ADDRESS_MQ3)

mq3.config_cycle_time(mqx.CYCLE_TIME_32)
#in this example, we test alcohol concentration.
mq3.set_slope(mqx.MQ3_ALCOHOL_SLOPE)
mq3.set_intercept_y(mqx.MQ3_ALCOHOL_INTERCEPT_Y)

# we have calibrated Ro value in our envirenment.
mq3.set_Ro(mqx.MQ3_RO)

#you also can recalibrate Ro with method: calibrate_Ro
#mq3.calibrate_Ro(mqx.MQ3_RATIO_AIR)

try:
    while True:
        ppm = mq3.calibrate_ppm()
        print("ppm:{:.2f}".format(ppm))
        time.sleep(5)

except KeyboardInterrupt:
    None


