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

while True:
    (lat, lon, alt, hdop) = gps.position()
    print("%s %s %s %s" %(lat, lon, alt, hdop))
    if (str(lat) == 'None'):
        led.setLED('red')
        print("I do not have a fix!")
    else:
        led.setLED('green')
        print("%s, %s, %s, %s" %(lat, lon, alt, hdop))
    time.sleep(10)
