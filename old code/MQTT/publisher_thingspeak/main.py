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

channel_id = "Your_Channel_ID"
api_key = "Your_API_Write_Key"

broker_addr = "mqtt.thingspeak.com"
#MYDEVID = "channels/" + channel_id + "/publish/field/field1/" + api_key + "/"

MYDEVID = "channels/" + channel_id + "/publish/" + api_key + "/"

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
    the_data_json = "field1=" + ujson.dumps(the_data) + "&status=MQTTPUBLISH"
    print (the_data_json)
    client.publish(MYDEVID, the_data_json)
    time.sleep(30)
