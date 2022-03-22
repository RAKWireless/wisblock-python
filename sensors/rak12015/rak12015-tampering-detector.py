import time
import Adafruit_ADS1x15
from datetime import datetime

'''
ads1115 using an I2C communication bus
'''
ADS1115_BUS = 0x1
ADS1115_ADDRESS = 0x48
ADS1115_MAX = 32767

'''
set a gain of 1 for reading voltages from 0 to 4.09V.
Or pick a different gain to change the range of voltages that are read:
  - 2/3 = +/-6.144V
  -   1 = +/-4.096V
  -   2 = +/-2.048V
  -   4 = +/-1.024V
  -   8 = +/-0.512V
  -  16 = +/-0.256V
'''
ADS1115_GAIN = 1
ADS1115_GAIN_REF = 4.096
# If RAK12015 is mounted to Wisblock slot 1 on RAK7391, set ADS1115_CHANNEL = 1
# If RAK12015 is mounted to Wisblock slot 2 on RAK7391, set ADS1115_CHANNEL = 3
ADS1115_CHANNEL = 1
# Frequency to read the status of RAK12015, bigger value will increase the chance of missing a vibration
DELAY_SEC = 0.5

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(address=ADS1115_ADDRESS, busnum=ADS1115_BUS)

try:
    while True:
        '''
        This value is a number that ranges from -32768 to 32767 on the 16-bit ADS1115,
        A value of 0 means the signal is at a ground (reference) level, 32767  means 
        it's at or higher than the maximum voltage value for the current gain.
        '''
        system_time = datetime.now().strftime('%Y%m%d %H:%M:%S -')
        value = round(adc.read_adc(ADS1115_CHANNEL, gain=ADS1115_GAIN) * ADS1115_GAIN_REF / ADS1115_MAX, 2)
        # Reading value close to 0 means there is no vibration
        # While non-zero values indicates that a vibration is detected
        if value == 0:
            print('%.2f' % value, "-All good")
        else:
            print('%.2f' % value, "-ALERT", system_time, "Vibration detected!")
        time.sleep(DELAY_SEC)
except KeyboardInterrupt:
    None
