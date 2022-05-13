# WisBlock-Python

A collection of examples to interface [WisBlock](https://github.com/RAKWireless/WisBlock) modules and sensors using Python.

# Hardware requirement

To be able to use the WisBlock module, the hardware must match the WisBlock form factor. Right now, RAKwireless provides two devices to support the WisBlock module for the Raspberry Pi platform. 

*   RAK7391

    RAK7391 is a powerful CM4 extension board. There are two WisBlock I/O connectors on the board already. Users can connect the WisBlock I/O module with RAK7391 directly. 

* RAK6421

    RAK6421 is a Pi HAT board that includes the WisBlock connector. Users can put the WisBlock module on the Pi HAT and plug it on the Raspberry Pi board. 


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
    * [RAK13600 NFC Reader Module](/interface/rak13600)   
    * [RAK14006 Rotary Input](/interface/rak14006)   
    * [RAK16001 ADC Module](/interface/rak16001)
    * [RAK17000 Motor Driver](/interface/rak17000)
* RAK7391

    * [ads1115  16-Bit ADC](/rak7391/ads1115)
    * [atecc608 Secure Element](/rak7391/atecc608)
    * [EEPROM](/rak7391/eeprom)
    * [PI4IOE5V96224 24-bits GPIO Expander](/rak7391/pi4ioesv962)
    * [TPT29555 16-bit GPIO Expander](/rak7391/tpt29555)
* Sensors
    * [RAK1901 Temperature and Humidity Sensor](/sensors/rak1901)
    * [RAK1902 Barometric Pressure Sensor](/sensors/rak1902)
    * [RAK1903 Ambient Light Sensor](/sensors/rak1903)
    * [RAK1906 Environmental Sensor](/sensors/rak1906)
    * [RAK12001 Fingerprint Sensor](/sensors/rak12001)
    * [RAK12004 MQ2 Gas Sensor](/sensors/rak12004)
    * [RAK12006 Pyroelectric Infrared Radial (PIR) module](/sensors/rak12006)
    * [RAK12009 MQ3 Gas Sensor](/sensors/rak12009)
    * [RAK12013 Radar Module](/sensors/rak12013)
    * [RAK12015 Vibration Sensor](/sensors/rak12015)
    * [RAK12019 UV sensor](/sensors/rak12019)
    * [RAK13003 IO Expansion Module](/sensors/rak13003)
    * [RAK16000 DC Current Sensor](/sensors/rak16000)
* Wireless
    * [RAK13300 SX1262 LPWAN Module](/wireless/rak13300)

## Copyright and license

Copyright (c) 2022 RAKwireless, under MIT License.


