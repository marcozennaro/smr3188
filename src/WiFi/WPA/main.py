from network import WLAN
import machine
import time
import ubinascii

wlan = WLAN(mode=WLAN.STA)

ssid = 'VodafoneZennaro'                        # <--- WIFI network name
password = 'Camilla2006'                   # <--- WIFI network password

nets = wlan.scan()
for net in nets:
    if net.ssid == ssid:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, password), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break


print(wlan.ifconfig())
print(ubinascii.hexlify(machine.unique_id(),':').decode())
