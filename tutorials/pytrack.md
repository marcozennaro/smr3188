# Pytrack: your exact position in the world

## Introduction
In this example, we will use a Lopy on a Pytrack board to access the position given by the internal GPS.

From Wikipedia: The Global Positioning System (GPS)is a space-based radionavigation system owned by the United States government and operated by the United States Air Force. It is a global navigation satellite system that provides geolocation and time information to a GPS receiver anywhere on or near the Earth where there is an unobstructed line of sight to four or more GPS satellites.

> To get a GPS fix (which means to get the exact position) you must have an unobstructed view of the sky. It will not work in the lab! You must use the Pytack outdoors.

The GPS does not require the user to transmit any data, and it operates independently of any telephonic or internet reception, though these technologies can enhance the usefulness of the GPS positioning information. The GPS provides critical positioning capabilities to military, civil, and commercial users around the world. The United States government created the system, maintains it, and makes it freely accessible to anyone with a GPS receiver.

## Learning outcomes

You will learn how to:
* access the position provided by the Pytrack GPS using Pycom high-level Python modules

## Required Components

For this example you will need:

- a LoPy module on a Pytack board
- a microUSB cable
- a development PC

The source code is in the `src/pytrack` directory.

> Always update the firmware to the most recent version.

## Using Pycom-provided high-level modules

In this lab, we will provide a simple example:

* reading GPS position `src/pytrack`


Pycom provides a library (a set of Python modules) abstracting the implementation details of the GPS. This library is already included in labs source code. If you want to download or fetch the last version of this libary, please refer to [workflow-and-setup.md](workflow-and-setup.md)

Let's take a look a the  `src/pytrack/main.py` first:

```python
import os
from pytrack import Pytrack
from L76GNSS import L76GNSS
import time
import LEDColors
import pycom

#Enable GPS here
py = Pytrack()
gps = L76GNSS(py, timeout=30)

# stop the heartbeat
pycom.heartbeat(False)
led = LEDColors.pyLED()

led.setLED('red')

(lat, lon, alt, hdop) = gps.position()
print("%s %s %s %s" %(lat, lon, alt, hdop))
```

You notice that it looks particularly simple and straightforward! That's the power of code abstraction and Python. 

Let's go trough each step:

1. first create a `Pytrack` object which will be used to communicate  between the microcontroller and the GPS board 

```python
py = Pytrack()
```

2. then create a `L76GNSS` object passing the previously created Pytrack object as argument, together with the timeout value of 30 seconds 
3. ​
```python
gps = L76GNSS(py, timeout=30)
```

3. and simply loop over measurements and readings every 10 seconds:

```python
while True:
    (lat, lon, alt, hdop) = gps.position()
    if (str(lat) == 'None'):
        led.setLED('red')
        print("I do not have a fix!")
    else:
        led.setLED('green')
        print("%s, %s, %s, %s" %(lat, lon, alt, hdop))
    time.sleep(10)
```

It's that easy!


## Exercises

1. Go out to get a GPS fix! Save the positions provided by the Pytrack in a file (call it log.cvs) and download it on your computer using the "Download" button in Atom.
2. Visualize the places you have visited using the instructions provided here: http://www.cartagram.com/5648/from-excel-to-google-maps/
