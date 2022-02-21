# PI4IOE5V96224 GPIO Expander library & usage example

[TOC]

## 1.Introduction

The RAK7391 has a 24bits [PI4IOESV96224](docs/PI4IOE5V96224.pdf) GPIO expander driven via I2C. This IC uses a simple SMBUS protocol to set and read the 24 pins ordered in 3 ports of 8 pins each.

## 2. Library

The `pi4ioesv96224.GPIOExpander` library takes care of reading and writing individual pins while keeping the status of the rest.

### 2.1. Constructor

The library consturctor accepts 3 parameters:

```
from pi4ioesv96224.pi4ioesv96224 import GPIOExpander
gpioe = GPIOExpander(bus, address, lazy)
```

* **bus** is the bus index (1 for the RAK7391)
* **address** is the address of the IC in the bus (0x20 for the RAK7391)
* **lazy** if True performs a read before any write to ensure the library cache in in sync with the IC, otherwise you must do it manually by calling `sync`.

### 2.2. Methods

* **reset** accepts a byte and sets all three ports to that value (0 turns all OFF, 255 turns all ON)
* **sync** syncs the internal cache to the IC
* **read** returns the current value from a given port and pin
* **write** sets the value of a given port and pin

## 3. Example

The [gpioe.py](gpioe.py) file is a command line utility that uses the `pi4ioesv96224` module in the background. You have several options:

List current status of all pins:

`python gpioe.py --all`

Set all pins ON:

`python gpioe.py --on`

Set all pins OFF:

`python gpioe.py --off`

Read a given port/pin:

`python gpioe.py -r <port> <pin>`

Write a given port/pin:

`python gpioe.py -w <port> <pin> <value>`

In the previous examples, <port> can be 0, 1 or 2, <pin> is a natural number from 0 to 7 and <value> is either 0 (off) or 1 (on).

You can combine several read and write actions (reads are executed first and write after reads):

`python gpioe.py -w 0 0 1 -w 0 1 1`



