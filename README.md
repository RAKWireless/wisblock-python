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
    * [RAK1921 OLED Display](/display/rak1921)
* Interface
    * [RAK5801 4-20mA Sensor](/interface/rak5801)
    * [RAK5802 RS485 Interface](/interface/rak5802)
    * [RAK5811 0-5V Sensor](/interface/rak5811)
    * [RAK13001 Relay](/interface/rak13001)
    * [RAK13004 PWM Module](/interface/rak13004)
    * [RAK13005 LINbus Interface](/interface/rak13005)
    * [RAK13007 Relay IO Module](/interface/rak13007)   
    * [RAK16001 ADC Module](/interface/rak16001)
    * [RAK17000 Motor Driver](/interface/rak17000)
* RAK7391
    * [ads1115 example](/rak7391/ads1115)
    * [gpio expander](/rak7391/gpio_expander)
* Sensors
    * [RAK12015 example](/sensors/rak12015)
    * [RAK16000 example](/sensors/rak16000)


