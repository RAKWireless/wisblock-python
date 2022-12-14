#!/usr/bin/env python3

__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "0.1.0"
__status__ = "Production"

from mimetypes import init
import smbus
import time

I2C_BUS = 0x1
I2C_ADDRESS = 0x51
VOLTAGE_REF = 5.0


#Address Pointer Register
REG_CONVERSION_RESULT = 0x00
REG_ALERT_STATUS =0x01
REG_CONFIGURATION =0x02
REG_LOW_LIMIT = 0x03
REG_HIGH_LIMIT = 0x04
REG_HYSTERESIS = 0x05
REG_LOWEST_CONVERSION = 0x06
REG_HIGEST_CONVERSION = 0x07

#Configuration Register
REG_CONFIG_ALERT_HOLD_MASK = 0x10
REG_CONFIG_ALERT_HOLD_CLEAR = 0xef
REG_CONFIG_ALERT_FLAG_NOCLEAR = 0x10

REG_CONFIG_ALERT_FLAG_MASK = 0x08
REG_CONFIG_ALERT_FLAG_DIS = 0xf7
REG_CONFIG_ALERT_FLAG_EN = 0x08

REG_CONFIG_ALERT_PIN_MASK = 0x04
REG_CONFIG_ALERT_PIN_DIS = 0xfb
REG_CONFIG_ALERT_PIN_EN = 0x04

REG_CONFIG_POLARITY_MASK = 0x01
REG_CONFIG_POLARITY_LOW = 0xfe
REG_CONFIG_POLARITY_HIGH = 0x01

CONFIG_CYCLE_TIME_MASK = 0xE0
AUTOMATIC_MODE_DISABLED = 0x00
CYCLE_TIME_32 = 0x20
CYCLE_TIME_64 = 0x40
CYCLE_TIME_128 = 0x60
CYCLE_TIME_256 = 0x80
CYCLE_TIME_512 = 0xA0
CYCLE_TIME_1024 = 0xC0
CYCLE_TIME_2048 = 0xE0

class ADC121C021:
    def __init__(self, bus=I2C_BUS, addr=I2C_ADDRESS):
        self._bus = bus = smbus.SMBus(bus)
        self._addr = addr

    def read_configure_register(self):
        return self._bus.read_byte_data(self._addr, REG_CONFIGURATION)

    def config_cycle_time(self, cycle_time):
        tmp = self.read_configure_register() & 0x1f
        tmp = tmp | cycle_time
        self._bus.write_byte_data(self._addr, REG_CONFIGURATION, tmp)
    
    def read_alert_status(self):
        data = self._bus.read_i2c_block_data(self._addr, REG_CONVERSION_RESULT, 2)
        if data[0] & 0x80:
            status = self._bus.read_byte_data(self._addr, REG_ALERT_STATUS)
            return status

    def clear_aler_staus(self):
        self._bus.write_byte_data(self._addr, REG_ALERT_STATUS, 0)

    def config_alert_hold(self, enable):
        tmp = self.read_configure_register()
        if enable:
            tmp = tmp | REG_CONFIG_ALERT_FLAG_NOCLEAR
        else:
            tmp = tmp | REG_CONFIG_ALERT_HOLD_CLEAR
        self._bus.write_byte_data(self._addr, REG_CONFIGURATION, tmp)
        

    def read_alert_hold(self):
        tmp = self.read_configure_register() & REG_CONFIG_ALERT_HOLD_MASK
        return tmp

    def config_alert_flag(self, enable):
        tmp = self.read_configure_register()
        if enable:
            tmp = tmp | REG_CONFIG_ALERT_FLAG_EN
        else: 
             tmp = tmp | REG_CONFIG_ALERT_FLAG_DIS
        self._bus.write_byte_data(self._addr, REG_CONFIGURATION, tmp)
    
    def read_alert_flag(self):
        return self.read_configure_register() & REG_CONFIG_ALERT_FLAG_MASK

    def config_alert_pin(self, enable):
        tmp = self.read_configure_register()
        if enable:
            tmp = tmp | REG_CONFIG_ALERT_PIN_EN
        else: 
             tmp = tmp | REG_CONFIG_ALERT_PIN_DIS
        self._bus.write_byte_data(self._addr, REG_CONFIGURATION, tmp)
    
    def read_alert_pin(self):
        return self.read_configure_register() & REG_CONFIG_ALERT_PIN_MASK

    def config_alert_polarity(self, polarity):
        tmp = self.read_configure_register()
        if polarity:
            tmp = tmp | REG_CONFIG_POLARITY_HIGH
        else: 
             tmp = tmp | REG_CONFIG_POLARITY_LOW
        self._bus.write_byte_data(self._addr, REG_CONFIGURATION, tmp)
    
    def read_alert_polarity(self):
        return self.read_configure_register() & REG_CONFIG_POLARITY_MASK

    def config_alert_low_threshold(self, threshold):
        threshold &= 0x0fff
        self._bus.write_word_data(self._addr, REG_LOW_LIMIT, threshold)

    def read_alert_low_threshold(self):
        tmp = self._bus.read_word_data(self._addr, REG_LOW_LIMIT)
        tmp &= 0x0fff
        return tmp

    def config_alert_high_threshold(self, threshold):
        threshold &= 0x0fff
        self._bus.write_word_data(self._addr, REG_HIGH_LIMIT, threshold)

    def read_alert_high_threshold(self):
        tmp = self._bus.read_word_data(self._addr, REG_HIGH_LIMIT)
        tmp &= 0x0fff
        return tmp

    def config_hysteresis(self, hysteresis):
        hysteresis &= 0x0fff
        self._bus.write_word_data(self._addr, REG_HYSTERESIS, hysteresis)

    def read_hysteresis(self):
        tmp = self._bus.read_word_data(self._addr, REG_HYSTERESIS)
        tmp &= 0x0fff
        return tmp
    
    def read_lowest_conversion(self):
        tmp = self._bus.read_word_data(self._addr, REG_LOWEST_CONVERSION)
        tmp &= 0x0fff
        return tmp
        
    def clear_lowest_conversion(self):
        self._bus.write_word_data(self._addr, REG_LOWEST_CONVERSION, 0x0fff)

    def read_highest_conversion(self):
        tmp = self._bus.read_word_data(self._addr, REG_HIGEST_CONVERSION)
        tmp &= 0x0fff
        return tmp

    def clear_highest_conversion(self):
        self._bus.write_word_data(self._addr, REG_HIGEST_CONVERSION, 0x0fff)

    def read_adc_value(self):
        data = self._bus.read_i2c_block_data(self._addr, REG_CONVERSION_RESULT, 2)
        raw_value = (data[0] & 0x0F) * 256 + data[1]
        return raw_value
    def read_adc_voltage(self):
        raw_value = self.read_adc_value()
        voltage = raw_value * VOLTAGE_REF / 4095.0
        return voltage

'''
if __name__ == '__main__' :
    adc = ADC121C021()
    adc.config_cycle_time(CYCLE_TIME_32)
    time.sleep(0.5)
    while True:
        print(adc.read_adc_voltage())
        time.sleep(0.5)
'''
