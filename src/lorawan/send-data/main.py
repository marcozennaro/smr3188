from network import LoRa
import time
import binascii
import socket
import time

lora = LoRa(mode=LoRa.LORAWAN, tx_power=14, region=LoRa.EU868)

app_eui = binascii.unhexlify('INSERTAPPEUI')
app_key = binascii.unhexlify('INSERTAPPKEY')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(5)
    print('Not joined yet...')

print('Network joined!')

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)

while True:
    s.send(bytes([1, 2, 3]))
    #s.settimeout(3.5)
    print("Packet sent!")
    time.sleep(30) # wait for the tx and rx to complete
    rx_pkt = s.recv(64)   # get the packet received (if any)
    print(rx_pkt)
