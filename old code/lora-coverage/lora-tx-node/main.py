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
lora = LoRa(mode=LoRa.LORA, tx_power=14, region=LoRa.EU868, frequency=865062500)

# Use frequencies for Nepal
lora.remove_channel(1)
lora.remove_channel(2)
lora.remove_channel(3)

lora.add_channel(1, frequency=865062500, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=865402500, dr_min=0, dr_max=5)
lora.add_channel(3, frequency=865985000, dr_min=0, dr_max=5)

# Get loramac as id to be sent in message
lora_mac = binascii.hexlify(network.LoRa().mac()).decode('utf8')

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

count_tx = 0

pycom.heartbeat(False)

# tx loop
while True:
    s.setblocking(True)
    pycom.rgbled(0x7f7f00) # yellow
    msgtx = 'Message from node '+ str(lora_mac)
    crc8 = utils.crc(msgtx.encode('utf8'))
    msgtx2 = msgtx + ',' + crc8

    s.send(msgtx)
    print('Tx: {} '.format(msgtx) + ' sent')

    count_tx += 1

    # Get any data received...
    s.setblocking(False)
    data = s.recv(64)
    pycom.rgbled(0x007f00) # green
    time.sleep(2)
