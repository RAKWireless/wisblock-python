# RAKMQ Python Library

## 1.Introduction

 MQ-x is a serial of gas sensors for detecting the different kinds of gases concentration. RAKWireless  integrate MQ-x and ADC121C021 in the WisBlock Modules. this python library is developed for RAK's MQ-x sensors. now this library is compatible with MQ-2 and MQ-3.

### 1.1.MQ-2

The **MQ-2 Gas sensor** can detect or measure gasses like LPG, Alcohol, Propane, Hydrogen, CO, and even methane. the module version of this sensor comes with a Digital Pin which makes this sensor to operate even without a microcontroller and that comes in handy when you are only trying to detect one particular gas. when it comes to measuring the gas in ppm the analog pin has to be used, the analog pin also TTL driven and works on 5V and hence can be used with most common microcontrollers.

### 1.2.MQ-3B

MQ-3B gas sensor has high sensitivity to alcohol gas and can resistant to the interference of gasoline, smoke and vapour. It is with low cost and suitable for various applications of detecting alcohol at different concentration. for more details, you can refer to [MQ-3B datasheet](docs/MQ-3B.pdf)

### 1.3.ADC121C021

ADC121C021 is a 1-Channel 12-Bit Analog to Digital Converter with a I2C Interface and 0-5VDC Input Voltage Range.

### 2.Library

This python library develop two class. `class ADC121C021`  offer a series of method for an ADC121C021 chip. you can easily configure ADC121C021 using this library and read the voltage. `class MQx` is from `class ADC121C021` inheritance, used to convert voltage to ppm of gas.

### 2.1.class ADC121C021

The  `class ADC121C021` constructor accepts 2 parameters:

```
 def __init__(self, bus=I2C_BUS, addr=I2C_ADDRESS):
        self._bus = bus = smbus.SMBus(bus)
        self._addr = addr
```

* **bus** is the bus index (1 for the RAK7391)
* **address** is the address of the IC in the bus (0x51 for the RAK7391)

Most of method are used to configure ADC121C021 chip or get configuration status by writing/reading a specific register,  you can get more details form [ADC121C021 datasheet](docs/adc121c021.pdf). the methods we use the most:

- **set_cycle_time**  configure automatic conversion mode. when value is set to zero, the automatic conversion mode is disabled. 
- **read_adc_value**  read the raw value from ADC121C021, the range of value should be 0-4095
- **read_adc_voltage**  convert the raw value to actual voltage

### 2.2.class MQx

The `class MQ-x` offers methods , which convert voltage to ppm by some mathematical model calculation.

detailed calculation method can be referred to:[How Do Gas Sensors Work](https://jayconsystems.com/blog/understanding-a-gas-sensor)

- **calibrate_Ro** we can get the sensitivity characteristics graph from [MQ-2](docs/MQ-2.pdf) and [MQ-3B](docs/MQ-3B.pdf) datasheet.  we can see the resistance ratio in air is a constant, so we can calibrate Ro in an air environment

- **calibrate_ppm** in the sensitivity characteristics graph, we will treat the lines as if they were linear, so we can use one formula that linearly relates the ratio and the concentration.`self._slope` is slope of the line, `self._intercept_y` is the intercept of Y coordinate. you can calibrate them from the sensitivity characteristics graph for each gas.

## 3.Example

```
from mqx import mqx
import time

mq2 = mqx.MQx(bus=mqx.I2C_BUS, addr=mqx.I2C_ADDRESS_MQ2)
mq2.config_cycle_time(mqx.CYCLE_TIME_32)

#in this example, we test ppm of smoke.
mq2.set_slope(mqx.MQ2_SMOKE_SLOPE)
mq2.set_intercept_y(mqx.MQ2_SMOKE_INTERCEPT_Y)

# we have calibrated Ro value in our envirenment.
mq2.set_Ro(mqx.MQ2_RO)
#you also can recalibrate Ro with method: calibrate_Ro
#mq2.calibrate_Ro(mqx.MQ2_RATIO_AIR)

try:
    while True:
        ppm = mq2.calibrate_ppm()
        print("ppm: {:.2f}".format(ppm))
        time.sleep(5)

except KeyboardInterrupt:
    None

```

