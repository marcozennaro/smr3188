import machine
from network import WLAN
import time
import socket
import utime
from machine import SD
from pytrack import Pytrack
import LEDColors
import pycom
from L76GNSS import L76GNSS

print('start pytrack LOGGER')

# stop the heartbeat
pycom.heartbeat(False)
led = LEDColors.pyLED()

# start the PyTrack GPS
py = Pytrack()


# set the LED to red until the position is fixed
led.setLED('red')

# Writing a file in /flash folder
file_path = '/flash/log'

try:
    os.listdir('/flash/log')
    print('/flash/log file already exists.')
except OSError:
    print('/flash/log file does not exist. Creating it ...')
    os.mkdir('/flash/log')

name = '/rssi-wifi.log'

wlan = WLAN(mode=WLAN.STA, antenna=WLAN.INT_ANT)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'apricot':
        print('Network found!')
        time.sleep(1)
        wlan.connect(net.ssid, auth=(net.sec, 'wireless'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

#rtc = machine.RTC()
#rtc.init((2015, 1, 1, 1, 0, 0, 0, 0))
#print("Before network time adjust", rtc.now())
#print('Setting RTC using Sodaq time server')
#time.sleep(2)
#s=socket.socket()
#addr = socket.getaddrinfo('time.sodaq.net', 80)[0][-1]
#s.connect(addr)
#s.send(b'GET / HTTP/1.1\r\nHost: time.sodaq.net\r\n\r\n')
#ris=s.recv(1024).decode()
#s.close()
#rows = ris.split('\r\n')            # transform string in list of strings
#seconds = rows[9]
#print("After network time adjust")
#rtc.init(utime.localtime(int(seconds)))
#print(rtc.now())

#wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

count_rx = 0

while True:
    for net in nets:
        if net.ssid == "apricot":
                led.setLED('green')
                # get gps coordinates
                l76 = L76GNSS(py, timeout=10)
                coord = l76.coordinates()
                if (coord[0] == None):
                    lat = 'None'
                else:
                    #lat = "{}".format(coord[0]).encode('utf8')
                    lat = "{}".format(coord[0])
                if (coord[1] == None):
                    lon = 'None'
                else:
                    #lon = "{}".format(coord[1]).encode('utf8')
                    lon = "{}".format(coord[1])
                #if (coord[0] == None):
                    #led.setLED('red')                       # color red (no gps position)
                #else:
                    #led.setLED('green')                       # got gps position
                count_rx += 1

                with open(file_path + name, 'a') as f:
                    f.write(str(count_rx) + "," + str(net.rssi) + "," + str(lat) + "," + str(lon) + '\n')
                print(count_rx,",",lat, ",", lon, ",", net.rssi)
                time.sleep(1)
