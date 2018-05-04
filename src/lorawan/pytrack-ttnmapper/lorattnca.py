#   Class lorattnca TTN-Cayenne
#   Wrapper for LoRa communication
#   Based on this project:
#   https://github.com/puthli/meet-de-klas
#   Version 1.0
# mod 19/03:
# set lora connection to the things network / cayenne
#
#
from network import LoRa
import socket
import time
import binascii
import pycom
from CayenneLPP import cayenneLPP
import LEDColors

class LoRaTTNcayenne:
    # --------------------------------------
    # Initialize LoRa in LORAWAN.

    # reg=LoRa.EU868                  # def.: region=LoRa.EU868
    # freq=868000000                  # def.: frequency=868000000         
    # tx_pow=14                       # def.: tx_power=14                 
    # band=LoRa.BW_125KHZ             # def.: bandwidth=LoRa.868000000    
    # spreadf=8                       # def.: sf=7                        
    # prea=8                          # def.: preamble=8                  
    # cod_rate=LoRa.CODING_4_5        # def.: coding_rate=LoRa.CODING_4_5 
    # pow_mode=LoRa.ALWAYS_ON         # def.: power_mode=LoRa.ALWAYS_ON   
    # tx_iq_inv=False                 # def.: tx_iq=false                 
    # rx_iq_inv=False                 # def.: rx_iq=false                 
    # ada_dr=False                    # def.: adr=false                   
    # # pub=True                      # def.: public=true                 
    # pub=False                       # def.: public=true                 
    # tx_retr=1                       # def.: tx_retries=1                
    # dev_class=LoRa.CLASS_A          # def.: device_class=LoRa.CLASS_A   
    # 
    # # connection to lorawan
    # lora = LoRa(mode=LoRa.LORAWAN,
    #         region=reg,
    #         frequency=freq,         
    #         tx_power=tx_pow,               
    #         bandwidth=band,    
    #         sf=spreadf,                       
    #         preamble=prea,               
    #         coding_rate=cod_rate,
    #         power_mode=pow_mode,  
    #         tx_iq=tx_iq_inv,                
    #         rx_iq=rx_iq_inv,                
    #         adr=ada_dr,                  
    #         public=pub,       
    #         tx_retries=tx_retr,              
    #         device_class=dev_class)
    lora = LoRa(mode=LoRa.LORAWAN, tx_power= 14, region=LoRa.EU868)
    
    led = LEDColors.pyLED()
    app_eui = ""
    app_key = ""

    # start connection setting the thingsnetwork keys
    def start(self, force_join = False, str_eui = '70B3D57ED000A81D', str_key = '21BBB6C735F5B9BC2CEC7EF9B997B578'):

        print('LoRa start connection')
        # restore previous state
        if not force_join:
            self.lora.nvram_restore()

        # OTA authentication params
        self.app_eui = binascii.unhexlify(str_eui.replace(' ',''))
        self.app_key = binascii.unhexlify(str_key.replace(' ',''))
    
        # connection to the thingsnetwork
        self.led.setLED('red')

        if not self.lora.has_joined() or force_join == True:
            # join TTN
            self.lora.join(activation=LoRa.OTAA, auth=(self.app_eui, self.app_key), timeout=0)
            # wait until the module has joined the network
            while not self.lora.has_joined():
                print('Lorawan not joined yet....')
                # Not joined yet...
                time.sleep(2.5)

            # saving the state
            self.lora.nvram_save()
            
            # returning whether the join was successful
            if self.lora.has_joined():
                # Network joined!
                print('LoRa Joined')
                self.led.setLED('blue')
                time.sleep(1)
                self.led.setLED('off')
            else:
                # Network not joined!
                print('LoRa Not Joined')
                self.led.setLED('red')
                time.sleep(1)
                self.led.setLED('off')
            return self.lora
        else:
            print('LoRa Joined with force_join==False')
            self.led.setLED('blue')
            time.sleep(1)
            self.led.setLED('off')

    def cayenne(self):
        # set cayenne lpp packet
        #
        # create a LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket
        # s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0) # set the LoRaWAN data rate
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        s.setblocking(True)
        self.led.setLED('blue')
        # creating Cayenne LPP packet
        lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)
        return lpp

    # Get loramac of device
    def getLoraMac(self):
        return (binascii.hexlify(self.lora.mac()).upper().decode('utf-8'))
