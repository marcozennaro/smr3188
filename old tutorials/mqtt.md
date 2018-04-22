> [Internet of Things (IoT) | Training Course](mqtt.md) ▸ **MQTT**

# MQTT (Message Queue Telemetry Transport)

> Sending data to a public MQTT broker via WiFi

This lab is organized so that you can have an hands-on experience with MQTT and learn how to publish data to public MQTT brokers and how you can visualize your data using Thingspeak. 

To this end you will use:
1. a "sandbox" broker
1. the ThingSpeak broker

Among other things you will:
1. produce data by code using the LoPy devices
1. produce data to your own channel in ThingSpeak

## Hardware
Each group will use:
* A LoPy connected through a PySense board




## Public MQTT brokers
There are various public brokers, also called `sandboxes`. For example:
* `iot.eclipse.org`
    * more infos at: https://iot.eclipse.org/getting-started#sandboxes
* `test.mosquitto.org`
    * more infos at: http://test.mosquitto.org/
* `broker.hivemq.com`
    * more infos at: http://www.hivemq.com/try-out/
        * http://www.mqtt-dashboard.com/
        
we will always access them through the `1883`. 

The lab code is based on the `test.mosquitto.org` broker, but you can of course any other.

## A simple publisher

As a first example, let's generate some random data and send it to the public mosquitto broker. 

The source code is in the `src/MQTT/publisher` directory.


```python
from network import WLAN
from mqtt import MQTTClient
import machine
import time
import pycom

import ucrypto
import math
import ujson

wifi_ssid = "MyAP"
wifi_passwd = "MyPassword"

broker_addr = "test.mosquitto.org"
MYDEVID = "apricot"

def settimeout(duration):
   pass

def random_in_range(l=0, h=1000):
    r1 = ucrypto.getrandbits(32)
    r2 = ((r1[0]<<24) + (r1[1]<<16) + (r1[2]<<8) + r1[3]) / 2**32
    return math.floor(r2*h + l)

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return random_in_range()

def on_message(topic, msg):
    # just in case
    print("topic is: " + str(topic))
    print("msg is: " + str(msg))

pycom.heartbeat(False) # Disable the heartbeat LED

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == wifi_ssid:
        print("Network " + wifi_ssid + " found!")
        wlan.connect(net.ssid, auth=(net.sec, wifi_passwd), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print("WLAN connection succeeded!")
        print (wlan.ifconfig())
        break

client = MQTTClient(MYDEVID, broker_addr, 1883)

if not client.connect():
    print ("Connected to broker: " + broker_addr)

print("Sending messages ...")

while True:
    # creating data from random numbers
    the_data = get_data_from_sensor()

    # publishing the data
    the_data_json = ujson.dumps(the_data)
    client.publish(MYDEVID + "/value", the_data_json)
    time.sleep(10)

```

Check if the data has been sent correctly by using one of the many MQTT clients and by subscribing to the topic you have just created. For example you can use [MQTT.fx](http://mqttfx.jensd.de/) which is a MQTT Client written in Java based on Eclipse Paho. 

## Exercise
Read a value from the PySense (temperature, for example) and send it via MQTT to the public broker. Check with a client software if the data has arrived correctly.


## Accessing ThingSpeak via MQTT

ThingSpeak is an IoT analytics platform service that allows you to aggregate, visualize and analyze live data streams in the cloud. ThingSpeak provides instant visualizations of data posted by your devices to ThingSpeak. With the ability to execute MATLAB® code in ThingSpeak you can perform online analysis and processing of the data as it comes in. 


### Creating a *channel*
You first have to sign in. Go to https://thingspeak.com/users/sign_up and create your own account. 

Once you have logged in, you can create your first channel. For example:

![](https://i.imgur.com/nN8iyWl.png)

Copy the Channel ID as we will use it to publish data to this specific channel.

In the "Private View" section you can get an overview of your data (it's empty at the beginning!):
![](https://i.imgur.com/DzkbXVF.png)

Take a look to the other  sections. To be able to send data via MQTT, you need the data in the API Keys section. In my case it says:

![](https://i.imgur.com/BlfIqlK.png)

Copy the Write API Key as we will need it to publish data via MQTT.

Anyway, let's publish to a channel field feed using the infos that you can find here
https://es.mathworks.com/help/thingspeak/publishtoachannelfieldfeed.html.

This picture shows how the system works:

![](https://i.imgur.com/f4vfCTZ.png)

The source code is in the `src/MQTT/publisher_thingspeak` directory.

### Exercise
Once you have been able to send the randomly-generated data to Thingspeak, try to send data from the Pysense. As a second step, try to send more than one streams of data (temperature and humidity, for example).

> Keep in mind that the message update interval limit is 15 seconds for free accounts.