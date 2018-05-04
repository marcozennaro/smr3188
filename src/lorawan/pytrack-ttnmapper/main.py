# ---------------------------------------------------
# pytrack tx messages with lora-mac for ogs experiment
# Connection to the thingsnetwork
# No used deepsleep
#
# About loramac, see:
#
#https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/lora-mac.html
#
#https://forum.pycom.io/topic/934/lora-stats-documentation-is-missing-the-parameter-must-passed/2
# https://github.com/puthli/meet-de-klas
#
#https://forum.pycom.io/topic/1648/how-to-recognize-awakening-from-pysense-go-to-sleep/4
# machine.reset_cause() restituisce sempre un codice errato !!!!
# 05/10
# inserito watchdog
# https://docs.pycom.io/chapter/firmwareapi/pycom/machine/WDT.html
# ---------------------------------------------------
#
import array

import network
from network import LoRa
from network import WLAN
import lorattnca
import socket
import os
import binascii
import time
import utime
import math
import pycom
import machine
from machine import SD
from machine import WDT
from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
import sys
import LEDColors
from CayenneLPP import cayenneLPP

import gc

# from ttnmapper.py
#
def GpsForTTNmapper(sock, n_latitude, n_longitude, n_altitude, n_hdop):
   """Encode current position, altitude and hdop and send it using
LoRaWAN"""

   data = array.array('B', [0, 0, 0, 0, 0, 0, 0, 0, 0])

   lat = int(((n_latitude + 90) / 180) * 16777215)
   data[0] = (lat >> 16) & 0xff
   data[1] = (lat >> 8) & 0xff
   data[2] = lat & 0xff

   lon = int(((n_longitude + 180) / 360) * 16777215)
   data[3] = (lon >> 16) & 0xff
   data[4] = (lon >> 8) & 0xff
   data[5] = lon &0xff

   alt = int(n_altitude)
   data[6] = (alt >> 8) & 0xff
   data[7] = alt & 0xff

   hdop = int(n_hdop * 10)
   data[8] = hdop & 0xff

   message = bytes(data)
   count = sock.send(message)
   # return message

# ----------------------------------------------------

# start main
# stop the heartbeat
pycom.heartbeat(False)
led = LEDColors.pyLED()

time.sleep(2)
gc.enable()
print('start pytrack LOGGER')

#----------------------------------------------
# mount sd
#sd = SD()
#os.mount(sd, '/sd')
#----------------------------------------------

# disable WiFi
wlan = WLAN()
wlan.deinit()

connection = lorattnca.LoRaTTNcayenne()
time.sleep(2)
gc.enable()

py = Pytrack()
l76 = L76GNSS(py, timeout=30)   # GSP timeout set to 30 seconds
li = LIS2HH12(py)               # accelerometer

# start watchdog
wdt = WDT(timeout=120000)       # enable watchdog with a timeout of 120
seconds

count_tx = 0

# --------------------------------------
# start LoRa in LORAWAN mode, to connect to the thingsnetwork.
# Connessione per cayenne
# connection.start(force_join = False, str_eui = '70B3D57ED000AF3E',
str_key = '2F7022AA819A2469653F1B6DE7889C13')
# connessione per TTNMapper

APP_EUI = 'INSERTAPPEUI'
APP_KEY = 'INSERTAPPKEY'

if( APP_EUI == 'INSERTAPPEUI' or APP_KEY == 'INSERTAPPKEY'):
   lora = LoRa(mode=LoRa.LORAWAN)
   print("Register the following device EUI with the application and
disable Frame counter check in the settings.")
   print(binascii.hexlify(lora.mac()).upper().decode('utf-8'))
   print("Now enter the INSERTAPPEUI and INSERTAPPKEY above")
else:
   connection.start(force_join = False, str_eui = APP_EUI, str_key =
APP_KEY)

############################################################################
#main execution loop, triggered by awakening from deep sleep

# Get loramac as id to be sent in message
lora_mac = connection.getLoraMac()
lora_id = lora_mac[-6:]                     # only last 6 chars

ledcolor = 'red'                            # first start with color red
# no gps position)

while True:
   # -----------------------------
   gc.collect()

   wdt.feed()                                              # Feed the
#WDT to prevent it from resetting the system

   # --------------- start of code executed after awakening
   # led.setLED('green')
   led.setLED(ledcolor)

   # prepare msg to send
   # count_tx = pycom.nvs_get('count_tx')      # retrieve count_tx

   # ----------------------------
   gc.collect()
   wdt.feed()                                  # Feed the WDT to
# prevent it from resetting the system

   acc = li.acceleration()                     # read accelerometer
#parameters

   acc = li.acceleration()                     # read accelerometer parameters
   rol = li.roll()
   pit = li.pitch()
   # yaw = li.yaw()                            # 19/03: not used

   # ----------------------------
   gc.collect()
   wdt.feed()                                  # Feed the WDT to
#prevent it from resetting the system

   coord = l76.coordinates()                   # get gps coordinates
   # lat = str(coord[0])
   # lon = str(coord[1])

   # altitude (predisposition)
   alt = "{:.4f}".format(0.0)
   fAlt = 0.0
   fLat = 0.0
   fLon = 0.0
   if (coord[0] == None) :
       alt = 'None'
       lat = 'None'
       lon = 'None'
       fAlt = None
       fLat = None
       fLon = None
   else:
       lat = "{:.4f}".format(coord[0])
       # lat = "{:.4f}".format(coord[0]).encode('utf-8')
       fLat = float(coord[0])
   if (coord[1] == None):
       alt = 'None'
       lat = 'None'
       lon = 'None'
       fAlt = None
       fLat = None
       fLon = None
   else:
       lon = "{:.4f}".format(coord[1])
       fLon = float(coord[1])
       # lon = "{:.4f}".format(coord[1]).encode('utf-8')
   # show on led if there is gps position
   if (coord[0] == None):
       ledcolor = 'red'                        # color red (no gps
position)
   else:
       ledcolor = 'green'                      # got gps position

   gc.collect()
   wdt.feed()                                  # Feed the WDT to
# prevent it from resetting the system

   # ----------------------------
   # creating Cayenne LPP packet with gps position
   gc.collect()
   wdt.feed()                                  # Feed the WDT to
# prevent it from resetting the system

   ## fLat = 45.7038           ## dbg
   if fLat is not None:
       # send gps position
       print("position: [{}],[{}],[{}]".format(fLat, fLon, fAlt))
       #
       # disabilitato: usare codice default
       # lpp = connection.cayenne()
       # ===
       # create a LoRa socket
       s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
       s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
       s.setblocking(True)
       GpsForTTNmapper(s, fLat, fLon, fAlt, 0)
       # GpsForTTNmapper(s, 45.7038, 13.7202, 0.0, 0)      ## dbg
       #### # creating Cayenne LPP packet
       #### lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)
       #### # ===
       #### lpp.add_gps(fLat, fLon, fAlt)
       #### # lpp.add_gps(45.7038, 13.7202, 0.0)
       #### # lpp.add_temperature(10)
       #### lpp.send(reset_payload = True)

   # ----------------------------
   # form the message to save on csv
   # see:
# https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
   # https://docs.python.org/3/library/string.html#formatstrings
   # ex: {: 5d} print 5 digits fill with space
   # msgSd = str(count_tx) + ',' + lora_mac + ',' + streset + ',' +
#cause + ',' + str(coord)
   # ok
   # msgSd = str(count_tx) + ',' + lora_id + ',' + str(coord)
   # note:
   # 5 char of index, for 5 seconds, the max index value is 99999. It
#restart after 5 days
   # msgSd = "{: 5d},{},({: >8},{: >8})".format(
   msgSd = "{:5d},{},({: >8},{: >8})".format(
           count_tx,
           lora_id,
           lat,
           lon).encode('utf-8')

   # print(msgSd)

   # update message to save in sd
   msgSd = msgSd + ",{: >10.5f},{: >10.5f}".format(rol,pit).encode('utf-8')

   # connection.lora.nvram_save()
   print('{}[{}]{}'.format(lora_id, msgSd, len(msgSd)))

   # increment count_tx and save result
   count_tx += 1

   # pycom.nvs_set('count_tx', count_tx)       # save count_tx
   gc.collect()
   wdt.feed()                                  # Feed the WDT to
# prevent it from resetting the system

   #----------------------------------------------
   # write on file
   # see:
# https://stackoverflow.com/questions/5214578/python-print-string-to-text-file
   # msgSd.decode("utf-8") delete b'' chars
   # f = open('/sd/loggps.csv', 'a+')
   #with open('/sd/loggps.csv', 'a+') as text_file:
#        text_file.write("{}\n".format(msgSd.decode("utf-8")))
#        text_file.close()
   #----------------------------------------------

   gc.collect()
   # loop time 5 sec
   time.sleep(15)
   led.setLED('off')
   time.sleep(15)       # sleep for 15 seconds

   # ---------------
   #
