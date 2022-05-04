# ADC121C021 Python Library

## 1.Introduction

ADC121C021 is a 1-Channel 12-Bit Analog to Digital Converter with a I2C Interface and 0-5VDC Input Voltage Range.  you might be interested in the datasheet for this chips:[ADC121C021 datasheet](docs/adc121c021.pdf).

## 2.Library

This python library develop `class ADC121C021`  offer a series of method for an ADC121C021 chip. you can easily configure ADC121C021 using this library and read the voltage.

### 2.1.Constructor

The  `class ADC121C021` constructor accepts 2 parameters:

```
 def __init__(self, bus=I2C_BUS, addr=I2C_ADDRESS):
        self._bus = bus = smbus.SMBus(bus)
        self._addr = addr
```

* **bus** is the bus index (1 for the RAK7391)
* **address** is the address of the IC in the bus (0x51 for the RAK7391)

### 2.2.Methods

Most of method are used to configure ADC121C021 chip or get configuration status by writing/reading a specific register,  you can get more details form [ADC121C021 datasheet](docs/adc121c021.pdf). the methods we use the most:

- **set_cycle_time**  configure automatic conversion mode. when value is set to zero, the automatic conversion mode is disabled. 

- **read_adc_value**  read the raw value from ADC121C021, the range of value should be 0-4095
- **read_adc_voltage**  convert the raw value to actual voltage



## 3.Example

```
import time
from adc121c021 import adc121c021
adc = adc121c021.ADC121C021()
adc.config_cycle_time(adc121c021.CYCLE_TIME_32)
time.sleep(0.5)

while True:
    voltage = adc.read_adc_voltage()
    print("Reading: {:.2f}V".format(voltage))
    time.sleep(0.5)
```

