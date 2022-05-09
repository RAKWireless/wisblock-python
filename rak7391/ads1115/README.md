# Read the specified ADC channel on the RAK7391

[TOC]

## 1.Introduction

The RAK7391 has an analog to digital converters named **ADS1115**. ADS1115 is  a high recision16-bit ADC with 4 channels.  it have a programmable gain from 2/3x to 16x so you can amplify small signals and read them with higher precision. You might be interested in the datasheet for this chips:[ADS1115 datasheet](https://cdn-shop.adafruit.com/datasheets/ads1115.pdf). 

This guide explain how to read a specified ads1115 channel on the rak7391 with python.

## 2. Libray & Example

ADS1115 use the an I2C communication protocol to read analog values and there is an existing python library [Adafruit ADS1x15 Python library](https://github.com/adafruit/Adafruit_Python_ADS1x15).The recommended way to do this is to use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create a isolated environment. To install `virtualenv` you just have to:

```plaintext
sudo apt install virtualenv
```

Once installed you can create the environment and install the dependencies (run this on the `ads1115` folder):

```plaintext
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

You can install the library from the Python package index with `pip` command.

```
pip install -r requirements.txt
```

Once installed you can run the example by typing:

```
python ads1115_read.py
```

The example code can be found in the [ads1115_read.py](ads1115_read.py) file, you can change some parameters to a proper value. It read the analog value from ADS1115 port 0 every second and output it. The example is meant to be used with a trimpot that outputs a value from 0 to 3.3V.

### I2C parameters

The i2c address of ads1115 on the rak7391 is 0x48 and the i2c bus index is 1 by default.

```
ADS1115_BUS = 0x1
ADS1115_ADDRESS = 0x48
```

### ADC parameters

**channel**-there are 4 input channels on the ads1115, the channel number is from 0 to 3.

`ADS1115_CHANNEL = 0` 

**gain** - a programmable gain amplifier (PGA) is implemented on the ads1115. the gain can be set to 2/3, 1, 2, 4, 8 and 16. set a gain of 1 for reading voltages from 0 to 4.09V or pick a different gain to change the range of voltages that are read:

  - 2/3 = +/-6.144V
  - 1 = +/-4.096V
  - 2 = +/-2.048V
  - 4 = +/-1.024V
  - 8 = +/-0.512V
  - 16 = +/-0.256V

`ADS1115_GAIN = 1`

**reference** - the reference voltage for that specific gain, so if you are selecting gain 1 above set the reference voltage to 4.096:

`ADS1115_GAIN_REF = 4.096`

**value** - the read value is a number that ranges from -32768 to 32767 on the 16-bit ADS1115, a value of 0 means the signal is at a ground (reference) level, 32767 means it's at or higher than the maximum voltage value for the current gain.

`value = adc.read_adc(ADS1115_CHANNEL, gain=ADS1115_GAIN)`







