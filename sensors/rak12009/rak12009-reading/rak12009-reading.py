#!/usr/bin/env python3
"""
Read a gas concentration using rak12009.
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "0.1.0"
__status__ = "Production"

import time
import RPi.GPIO as GPIO
import math
from adc121c021 import ADC121C021, CYCLE_TIME_32

I2C_BUS = 0x1
I2C_ADDRESS = 0x55
VOLTAGE_REF = 5
RL = 10
RO = 16.1
RATIO_AIR = 1
ALCOHOL_SLOPE = -0.888
ALCOHOL_INTERCEPT_Y = 0.738

# EN_PIN is Power enable pin (active high)
# RAK6421 IO Slot#1: EN_PIN = 12
# RAK6421 IO Slot#2: EN_PIN = 22

EN_PIN = 12


'''
The sensitivity characteristics of the MQ-3 (shown as Fig.3 in datasheet) tells us 
the concentration of a gas in part per million (ppm) according to the resistance ratio 
of the sensor (RS/R0). RS is the resistance of the sensor that changes depending on the 
concentration of gas, and R0 is the resistance of the sensor at a known concentration 
in fresh air. From the graph, we can see that the resistance ratio in fresh air is a constant: 

    RS / R0 = 1 ppm

To calculate R0 we will need to find the value of the RS in fresh air. This will be done 
by taking the analog average readings from the sensor and converting it to voltage.
    
From Test Circuit of the MQ-3(shown as Fig.2 in datasheet). 
We can derive a formula to find RS using Ohm's Law：

    I = VC / (RS+RL)  
    VRL = [VC / (RS + RL)] x RL 
    VRL = (VC x RL) / (RS + RL)

now we solve for RS:
    
    RS = [(VC x RL) / VRL] - RL

'''

def calibrate_Ro(adc, ratio_air):
    total = 0
    for i in range(100):
        total += adc.read_adc_voltage()
        volt = total / 100
    Rs_air = VOLTAGE_REF * RL / volt - RL
    Ro = Rs_air / ratio_air
    return Ro

'''
we will treat the sensitivity characteristics of the MQ-3 as if they were linear. This way 
we can use one formula that linearly relates the ratio and the concentration. By doing so, 
we can find the concentration of a gas at any ratio value even outside of the graph’s boundaries. 
The formula we will be using is the equation for a line, but for a log-log scale. 
The formula for a line is: 

  y = mx + b  

Where:

y: X value 
x: X value 
m: Slope of the line 
b: Y intercept

For a log-log scale, the formula looks like this:

  log(y) = m*log(x) + b

we need to choose 2 points in the sensitivity characteristics and calcaulate slope and Y intercept.
'''

def calculate_ppm(adc, Ro, intercept_y, slope):
    volt = adc.read_adc_voltage()
    Rs = VOLTAGE_REF * RL / volt - RL
    ratio = Rs / Ro
    ppm_log10 = (math.log10(ratio) - intercept_y) / slope
    ppm = math.pow(10, ppm_log10)
    return ppm

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.HIGH)
time.sleep(0.5)

adc = ADC121C021(bus=I2C_BUS, addr=I2C_ADDRESS)
adc.config_cycle_time(CYCLE_TIME_32)
#Before you measure gas concentration, you must calibrate RO in your environment.
ro = calibrate_Ro(adc, RATIO_AIR)

try:
    while True:
        ppm = calculate_ppm(adc, ro, ALCOHOL_INTERCEPT_Y, ALCOHOL_SLOPE)
        print("ppm:{:.2f}".format(ppm))
        time.sleep(5)
except KeyboardInterrupt:
    None


