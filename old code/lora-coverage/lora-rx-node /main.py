# ---------------------------------------------------
# tx messages with lora-mac
# see:
# loramac
# https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/lora-mac.html
# https://forum.pycom.io/topic/934/lora-stats-documentation-is-missing-the-parameter-must-passed/2

import network
from network import LoRa
import binascii
import socket
import machine
import time
import binascii
import sys
import utils # utilities module with CRC calculation
import pycom

# Initialize LoRa in LORA mode.
lora = LoRa(mode=LoRa.LORA, tx_power=5, region=LoRa.EU868, frequency=865062500)

# Use frequencies for Nepal
lora.remove_channel(1)
lora.remove_channel(2)
lora.remove_channel(3)

pycom.heartbeat(False)

print ("Waiting for packets...")

# tx loop
while True:
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    # receive up to 256 characters
    dataRx = s.recv(256)
    print (dataRx)
    # get lora stats (data is tuple)
    LoraStats = lora.stats()
    print(LoraStats)

    pycom.rgbled(0x7f7f00) # yellow
    time.sleep(2)
