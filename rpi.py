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
    for x in range(0, device_count):
        radio.openWritingPipe(TXMASTER[x])        
        syn_write = bool (radio.write(message))              
        if (syn_write == 1):                                            
            print("SYNC RADIO: ",x)
                                  

def Poll(): 
    piperead=0                                                                                
    for x in range(0, device_count):
        piperead=x+1 
        command = "POLL"
        message = list(command)                                  
        radio.openWritingPipe(TXMASTER[x])
        syn_write = bool (radio.write(message))              
        if (syn_write == 1):
            radio.openReadingPipe(piperead, RXMASTER[x])
            radio.startListening() 
            recv_buffer = []
            radio.read(recv_buffer, radio.getDynamicPayloadSize())
            print(str(recv_buffer))
            radio.stopListening()


  #radio.startListening()                                                                   
  #radio.stopListening()   
def signal_handler(sig, frame):
    GPIO.cleanup() # this ensures a clean exit 
    sys.exit(1)


TXMASTER = [[0xAA, 0xAA, 0xAA, 0xAA, 0xF1],[0xAA, 0xAA, 0xAA, 0xAA, 0xF2],[0xAA, 0xAA, 0xAA, 0xAA, 0xF3],[0xAA, 0xAA, 0xAA, 0xAA, 0xF4],[0xAA, 0xAA, 0xAA, 0xAA, 0xF5]]
RXMASTER = [[0xAA, 0xAA, 0xAA, 0xAA, 0x01],[0xAA, 0xAA, 0xAA, 0xAA, 0x02],[0xAA, 0xAA, 0xAA, 0xAA, 0x03],[0xAA, 0xAA, 0xAA, 0xAA, 0x04],[0xAA, 0xAA, 0xAA, 0xAA, 0x05]]

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

#radio.openWritingPipe(TX[0])
#radio.openReadingPipe(0, RX[0])
#radio.openReadingPipe(1, RX[1])
#radio.openReadingPipe(2, RX[2])
#radio.openReadingPipe(3, RX[3])
#radio.openReadingPipe(4, RX[4])


radio.printDetails()
radio.powerUp()
receivedMessage = []                          

device_count = 5      
cycle_number = 0 

  
while True: 
    signal.signal(signal.SIGINT, signal_handler)
    sendSync()
    time.sleep(0.1)
    Poll()
    time.sleep(1)                    
 
