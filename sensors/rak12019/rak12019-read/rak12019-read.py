#!/usr/bin/env python3
"""
Read ambient light or ultraviolet light data using the RAK12019 module
"""
__copyright__ = "Copyright 2022, RAKwireless"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"
__maintainer__ = "rakwireless.com"

import time
import board
from adafruit_ltr390 import LTR390, MeasurementDelay, Resolution, Gain

i2c = board.I2C()
ltr = LTR390(i2c)
# Options for resolution
# ltr.resolution = Resolution.RESOLUTION_13BIT
# ltr.resolution = Resolution.RESOLUTION_16BIT
# ltr.resolution = Resolution.RESOLUTION_17BIT
# ltr.resolution = Resolution.RESOLUTION_18BIT
# ltr.resolution = Resolution.RESOLUTION_19BIT
# ltr.resolution = Resolution.RESOLUTION_20BIT
print("Measurement resolution is", Resolution.string[ltr.resolution])

# Options for gain
# ltr.gain = Gain.GAIN_1X
# ltr.gain = Gain.GAIN_3X
# ltr.gain = Gain.GAIN_6X
# ltr.gain = Gain.GAIN_9X
# ltr.gain = Gain.GAIN_18X
print("Measurement gain is", Gain.string[ltr.gain])

# Options for measurement_delay
# ltr.measurement_delay = MeasurementDelay.DELAY_25MS
# ltr.measurement_delay = MeasurementDelay.DELAY_50MS
# ltr.measurement_delay = MeasurementDelay.DELAY_100MS
# ltr.measurement_delay = MeasurementDelay.DELAY_200MS
# ltr.measurement_delay = MeasurementDelay.DELAY_500MS
# ltr.measurement_delay = MeasurementDelay.DELAY_1000MS
# ltr.measurement_delay = MeasurementDelay.DELAY_2000MS

# Default resolution is 16 bit, default gain is 3x, default measurement delay is 100ms
print("Measurement delay is", MeasurementDelay.string[ltr.measurement_delay])
print("")

try:
    while True:
        print("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)
        # for shorter measurement delays you may need to make this sleep shorter to see a change
        time.sleep(1.0)

except KeyboardInterrupt:
    print("Keyboard interrupt, exit")
    exit()
