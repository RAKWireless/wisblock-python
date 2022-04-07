# Reading temperature and humidity using WisBlock sensor RAK1901

[TOC]

## 1. Introduction

This guide explains how to use the [WisBlock Sensor RAK1901](https://docs.rakwireless.com/Product-Categories/WisBlock/RAK12015/Overview/) in combination with RAK6421 Wisblock Hat or RAK7391 WisGate Developer Connect to  Reading temperature and humidity using Python. 

### 1.1. RAK1901

RAK1901 is a WisBlock Sensor which extends the WisBlock system with a Sensirion SHTC3 temperature and humidity sensor. A ready to use SW library and tutorial makes it easy to build up an environmental temperature and humidity data acquisition system.

### 1.2. SHTC3

The SHTC3 is a digital humidity and temperature sensor  designed especially for high-volume consumer electronics  applications. This sensor is strictly designed to overcome  conventional limits for size, power consumption, and  performance to price ratio in order to fulfill current and  future requirements. for more details, please refer to [SHTC3_datasheet](https://www.mouser.com/datasheet/2/682/seri_s_a0003561073_1-2291167.pdf).

## 2. Hardware

### 2.1. Sensor hardware

RAK7391 already has a SHTC3 sensor onboard, that means you don't need an additional RAK1901 if you use RAK7391 board, however, you also can use RAK1901 in combination with RAK6421 Wisblock Hat on when using a Raspberry Pi .

### 2.2. Connection diagram

In the following figure, we show you how RAK1901 is connected to RAK6421.

<img src="assets/setup.png" alt="setup" style="zoom:67%;" /> 



## 3. Software

The example code can be found in the [rak1901-read.py](rak1901-read.py) file. In order to run this， you will first have to install some required modules. The recommended way to do this is to use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create an isolated environment. To install `virtualenv` you just have to:

```
sudo apt install virtualenv
```

Once installed you can create the environment and install the dependencies (run this on the `rak1901-read` folder):

```
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

Once installed you can run the example by typing:

```
python rak1901-read.py
```

After that， you can leave the virtual environment by typing `deactivate`. To activate the virtual environment again you just have to `source .env/bin/activate` and run the script. No need to install the dependencies again since they will be already installed in the virtual environment.
