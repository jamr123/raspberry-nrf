import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import signal
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)


def sendSync():                                                                              
    command = "SYNC"
    message = list(command)
    print("Sent: {}".format(message))                            
    syn_write = bool (radio.write(message))                 
    if (syn_write == 0):                                            
        print(' syn write failed')   
                                  

def Poll():                                                                                 
     for x in range(0, device_count):                   # use 5 device now, so x = 0, 1, 2, 3, 4                  
         radio.openWritingPipe(slaveAddress[x])            
         dataToSend = bytearray([01])                   # if you like, you can change 01 to be a string or a character or anything
                                                        # please try to control "dataToSend". we can use it to poll specific arduino device's data
         time.sleep(0.05)                                   
         poll_write = bool (radio.write(dataToSend, 0))       
         if poll_write:     
             radio.openReadingPipe(x+1, slaveAddress[x])   
             radio.startListening()                         
             start_time =time.time()                        
             while(time.time()-start_time <0.02):            
                 if (radio.available()): 
                    receivedMessage = radio.read(radio.getDynamicPayloadSize())                   
                    x_int = (receivedMessage[1] << 8) + receivedMessage[0]
                    Measurements [x] = x_int
                    print(x_int)                  
         radio.stopListening() 
                                                                      
    
def signal_handler(sig, frame):
    GPIO.cleanup() # this ensures a clean exit 
    sys.exit(1)


TX = [[0xAA, 0xAA, 0xAA, 0xAA, 0xFF]]
RX = [[0xAA, 0xAA, 0xAA, 0xAA, 0x01],[0xAA, 0xAA, 0xAA, 0xAA, 0x02],[0xAA, 0xAA, 0xAA, 0xAA, 0x03],[0xAA, 0xAA, 0xAA, 0xAA, 0x04],[0xAA, 0xAA, 0xAA, 0xAA, 0x05]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)                         

radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x20)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(TX[0])
radio.openReadingPipe(0, RX[0])
radio.openReadingPipe(1, RX[1])
radio.openReadingPipe(2, RX[2])
radio.openReadingPipe(3, RX[3])
radio.openReadingPipe(4, RX[4])


radio.printDetails()
radio.powerUp()
receivedMessage = 0                          

device_count = 5      
cycle_number = 0 

  
while True: 
    signal.signal(signal.SIGINT, signal_handler)
    sendSync()
    time.sleep(1)                    
 
