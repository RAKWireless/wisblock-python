# WisBlock-Python

A collection of examples to interface [WisBlock](https://github.com/RAKWireless/WisBlock) modules and sensors using Python.

# Hardware requirement

To be able to use the WisBlock module, the hardware must match the WisBlock form factor. Right now, RAKwireless provides two devices to support the WisBlock module for the Raspberry Pi platform. 

## RAK7391

RAK7391 is a powerful CM4 extension board. There are two WisBlock I/O connectors on the board already. Users can connect the WisBlock I/O module with RAK7391 directly. 

## RAK6421

RAK6421 is a Pi HAT board that includes the WisBlock connector. Users can put the WisBlock module on the Pi HAT and plug it on the Raspberry Pi board. 

## Copyright and license

Copyright (c) 2022 RAKwireless, under MIT License.

# Examples

The repository structure follows that on the [RAKwireless store](https://store.rakwireless.com/pages/wisblock)

* Display
    * [RAK1921 OLED Display](/examples/oled)
* Interface
    * [RAK5801 4-20mA Sensor](/examples/rak5801)
    * [RAK5802 RS485 Interface](/examples/rak5802)
    * [RAK5811 0-5V Sensor](/examples/rak5811)
    * [RAK13001 Relay](/examples/rak13001)
    * [RAK13004 PWM Module](/examples/rak13004)
    * [RAK13005 LINbus Interface](/examples/rak13005)
    * [RAK16001 ADC Module](/examples/rak16001)
    * [RAK17000 Motor Driver](/examples/rak17000)
