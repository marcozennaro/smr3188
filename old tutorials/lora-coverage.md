> [Internet of Things (IoT) | Training Course](lora-coverage.md) ▸ **LoRa coverage**

# LoRa coverage: collecting and mapping RSSI and SNR

## Introduction
In this example, we want to produce a LoRA coverage map. The setup is the following:

* a fixed node will send messages over LoRa;
* on reception, a mobile node will:
    * determine **RSSI** (Receive Signal Strength Indicator) and **SNR** (Signal Noise Ratio) using messages received;
    * use the Pytrack module to gather GPS coordinates;
    * save the RSSI and the GPS data in a file to be analyzer and visualized online.


## Learning outcomes

You will learn how to:

* produce a LoRa coverage map.

## Required Components

For this example you will need:

- a LoPy module that will be used as a Transmitter (fixed position)
- a LoPy module that will be used as a Receiver (nomadic)
- a PyTrack module
- two microUSB cables
- a development PC
- an external battery to power the nomadic device.

The source code is in the `src/lora-coverage` directory.

> Always update the firmware to the most recent version.



## 1. Transmitter node setup
The sole responsibility of the transmitter node is to send LoRa packets (in this specific case with minimal information in it - device's MAC address).

You can find the source code to be synchronized to your Lopy in the following folder `src/lora-coverage/lora-tx-node` including:

* `boot.py`
* `utils.py` and
* `main.py` (below)


```python
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
```

## 2. Receiver node setup

The receiver node will measure the **RSSI** and **SNR**. There is a dedicated method in `LoRa class` named `lora.stats()` returning a named tuple with usefel information from the last received LoRa or LoRaWAN packet. The named tuple has the following form:

```
(rx_timestamp, rssi, snr, sftx, sfrx, sftx, tx_trials)
```
So the receiver know the timestamp of the received packet, the signal level, the signal to noise ratio, the spreading factor of the transmitter, the spreading factor of the receiver and the number of transmission trails.

You can find the source code to be synchronized to your Lopy in the following folder `src/lora-coverage/lora-rx-node` including:
* `boot.py`
* `utils.py` and
* `main.py` (below)


## Exercises

1. Update `main.py` of receiver node to change the LED color. For example you can switch it to orange when `RSSI < -100 dBm`, red when it is `RSSI < -110 dBm`, green when it is stronger than -110 dBm.

2. Form three teams. Each team will set up:

    * a transmitter (at a fixed location of your choice), using the frequencies reported below
    * 1-2 mobile nodes (receivers) 

LoRa network connections for both transmitters and receivers should be setup as follows:

| Team   |  Frequency (MHz)  |
| ------ | -----------------|
| 1      | 865.0625              |
| 2      | 865.4025             |
| 3      | 865.9850              |


[Please refer to TTN documentation for the frequency allocation for Nepal, which is the same as the one for India.](https://www.thethingsnetwork.org/wiki/LoRaWAN/Frequencies/Frequency-Plans)


3. In the receiving node, log the values of RSSI together with thre GPS positions in the flash memory. Use online tools such as GPS Visualizer to produce a coverage map.