from network import WLAN
import machine
import time
import ubinascii

wlan = WLAN(mode=WLAN.STA)
#wlan.ifconfig(config='dhcp')
nets = wlan.scan()

for net in nets:
    if net.ssid == 'nsrciot':
        print("network apricot found!")
        wlan.connect(net.ssid, auth=(net.sec, 'wireless'), timeout=5000)
        wlan.isconnected()
    break

print("I am here")
time.sleep(10)
print(wlan.ifconfig())
print(ubinascii.hexlify(machine.unique_id(),':').decode())
# nets = wlan.scan()
# for net in nets:
#     if net.ssid == 'nsrc':
#         print('Network found!')
#         wlan.connect(net.ssid, auth=(net.sec, 'wireless'), timeout=5000)
#         if  wlan.isconnected():
#             print('WLAN connection succeeded!')
#         break
#
# print(wlan.ifconfig())
