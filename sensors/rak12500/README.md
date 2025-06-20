# RAK12500 WisBlock GNSS Location Module

[TOC]

## 1. Introduction

This guide explains how to use the [RAK12500 WisBlock GNSS Location Module](https://docs.rakwireless.com/product-categories/wisblock/rak12500) in combination with RAK6421 Pi Hat and GPSd to share GPS information with any service in your Raspberry Pi.

Since GPSd does not have support for I2C GPS we will first create a service that will bridge the I2C interface in the RAK12500 to a serial socket and then connect the GPSd service to that same socket. Finally we will be able to read the data from the GPS using a local GPSd client, but any GPSd client will work. There are multiple integrations with different languages, UI tools and databases available.

## 2. Hardware

### 2.1. Sensor hardware

RAK12500 WisBlock GNSS Location Module extends the WisBlock system with a ZOE-M8Q module that supports HPS, GLONASS, QZSS and BeiDou. Its i2c address is `0x42`. 

You will also need a GPS antenna for the module.

### 2.2. RAK6421 Pi-Hat

RAK6421 WisBlock Pi Hat. The RAK6421 has 2 WisBlock IO slots and 4 WisBlock sensor slots, 2 of them are compatible with the RAK12500 (slots A and C).

### 2.3. A Raspberry Pi host

A Raspberry Pi 3/4/5 or CM carrier board with Raspberry Pi compatible header, like the RAK7391 WisGate Connect.

### 2.4. Connect everything

Steps:

* Connect RAK12500 to RAK6421 board on sensor slot A (it will also work on slot C). Use the screw to fix in place. 
* Attach the GPS uFL antenna to the RAK12500 module And then connect RAK6421 to your Raspberry Pi. Make sure the antenna points to the sky for better reception.
* Connect the RAK6421 Hat to a Raspberry Pi or RAK7391. 
* Flash the Raspberry Pi SD or the CM4/5 eMMC with Raspberry Pi OS or RAKPiOS.
* Boot the device and perform the initial setup (this will differ between different OS).
* Run through the steps in the Software section below to configure everything.

## 3. Software

### 3.1 Dependencies

The example relies on python3-smbus library, so we install it firstly along with the socat and gpsd utils.

```
sudo apt install python3-smbus2 socat gpsd
```

### 3.2 Test the service

The code can be found in the [rak12500-gpsd.py](./rak12500-gpsd.py) file.

```
I2C_BUS=1 I2C_ADDRESS=0x42 python3 ./rak12500-gpsd.py
```

If everything is correct, you should immediately see a bunch of NMEA sentences in the console. Just Ctrl+C to stop, and then continue with the remaining steps below. 

If not, you'll need to resolve whatever errors you see before proceeding.

### 3.3 Setup the systemd service (use the I²C bus and address of your GPS module):

We are using the socat utility to bridge the output of our python script to a serial socket then GPSd will be able to monitor. To make sure this is always available we create a service file to run the bridge on boot. Make sure the `WorkingDirectory` variable points to the folder where the `rak12500-gpsd.py` file. Then run the commands below:

```
chmod +x rak12500-gpsd.py
sudo cp rak12500-gpsd.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now rak12500-gpsd.service
```

### 3.4 Test we can read the output on the socket

```
sudo tail -f /dev/gpsd0
```

Again, you should be seing a bunch of NMEA sentences in the console. Just Ctrl+C to stop.

### 3.5 Test the GPSd service also reads the output

We will stop the GPSd service and test it manually first:

```
sudo systemctl stop gpsd
sudo systemctl stop gpsd.socket
sudo /usr/sbin/gpsd -n --readonly -N -D3 /dev/gpsd0
```
At this point the important bit is if the service recognizes the stream, you should see a line such as:

```
gpsd:INFO: /dev/gpsd0 identified as type NMEA0183, 1 sec @ 9600bps
```

Type Ctrl+C to stop the execution.

### 3.6 Configure the GPSd service

Edit the `/etc/default/gpsd` file as below

```
# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/gpsd0"

# Other options you want to pass to gpsd
GPSD_OPTIONS="-n --readonly"

# Automatically hot add/remove USB GPS devices via gpsdctl
USBAUTO="false"
```

### 3.7 Start the service

```
sudo systemctl start gpsd
```

### 3.8 Test the service

Now we will use a command line tool as client of the GPSd service. Any other GPSd client will work too.

```
cgpsd -s
```

The output will be something like this, hopefully with more satellites than the ones I see from my office :) :

```
┌───────────────────────────────────────────┐┌──────────────────Seen  9/Used  4┐
│ Time:        2025-06-19T14:43:59.000Z (0) ││GNSS   PRN  Elev   Azim   SNR Use│
│ Latitude:         XX.60269533 N           ││GP  3    3  49.0   61.0  27.0  Y │
│ Longitude:        XX.62396750 E           ││GP  4    4  81.0  111.0  15.0  Y │
│ Alt (HAE, MSL):        n/a,       n/a m   ││GP  6    6  34.0  313.0  33.0  Y │
│ Speed:             0.21 km/h              ││GP 17   17  39.0  236.0  27.0  Y │
│ Track (true, var):                n/a deg ││GP  1    1  36.0  131.0   0.0  N │
│ Climb:           n/a                      ││GP  7    7   0.0  177.0   0.0  N │
│ Status:         3D FIX (17 secs)          ││GP  9    9  52.0  215.0   9.0  N │
│ Long Err  (XDOP, EPX):  1.50, +/- 22.5 m  ││GP 11   11   1.0  312.0   0.0  N │
│ Lat Err   (YDOP, EPY):  1.58, +/- 23.7 m  ││GL 18   82   0.0    0.0   0.0  N │
│ Alt Err   (VDOP, EPV):  2.39, +/- 55.0 m  ││                                 │
│ 2D Err    (HDOP, CEP):  1.69, +/- 32.1 m  ││                                 │
│ 3D Err    (PDOP, SEP):  2.93, +/- 55.7 m  ││                                 │
│ Time Err  (TDOP):       3.77              ││                                 │
│ Geo Err   (GDOP):       6.47              ││                                 │
│ ECEF X, VX:              n/a    n/a       ││                                 │
│ ECEF Y, VY:              n/a    n/a       ││                                 │
│ ECEF Z, VZ:              n/a    n/a       ││                                 │
│ Speed Err (EPS):       +/-  170 km/h      ││                                 │
│ Track Err (EPD):        n/a               ││                                 │
│ Time offset:           -0.700744248 s     ││                                 │
│ Grid Square:            JN11ho44          ││                                 │
└───────────────────────────────────────────┘└─────────────────────────────────┘
```

## 4. License

We  share the project under MIT license.
