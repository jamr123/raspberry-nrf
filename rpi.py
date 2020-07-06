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
        command = "POLL"
        message = list(command)                                  
        radio.openWritingPipe(TXMASTER[x])
        syn_write = bool (radio.write(message))              
        if (syn_write == 1):
            radio.openReadingPipe(piperead, RXMASTER[x])
            radio.startListening() 
            recv_buffer = []
            start_time =time.time()                        
            while(time.time()-start_time <0.05):
                if (radio.available()): 
                    radio.read(recv_buffer, radio.getDynamicPayloadSize())
            radio.stopListening()

            stringdata=""
            for n in recv_buffer:
                stringdata+=chr(n)
            print(stringdata)
            #dts=stringdata.split("*") 
            #print('POLL FROM RADIO: ' + dts[0]  +' DATA: '+dts[1])     
            


  #radio.startListening()                                                                   
  #radio.stopListening()   
def signal_handler(sig, frame):
    GPIO.cleanup() # this ensures a clean exit 
    sys.exit(1)


TXMASTER = [[0xAA, 0xAA, 0xAA, 0xAA, 0xF0],[0xAA, 0xAA, 0xAA, 0xAA, 0xF1],[0xAA, 0xAA, 0xAA, 0xAA, 0xF2],[0xAA, 0xAA, 0xAA, 0xAA, 0xF3],[0xAA, 0xAA, 0xAA, 0xAA, 0xF4]]
RXMASTER = [[0xAA, 0xAA, 0xAA, 0xAA, 0x00],[0xAA, 0xAA, 0xAA, 0xAA, 0x01],[0xAA, 0xAA, 0xAA, 0xAA, 0x02],[0xAA, 0xAA, 0xAA, 0xAA, 0x03],[0xAA, 0xAA, 0xAA, 0xAA, 0x04]]

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



radio.printDetails()
radio.powerUp()
receivedMessage = []                          

device_count = 5      
cycle_number = 0 
print("\r\n\r\n")
  
while True: 
    
    signal.signal(signal.SIGINT, signal_handler)
    print("CYCLE: "+str(cycle_number ))
    print("SYNC >>>>>>") 
    sendSync()
    time.sleep(0.1)
    print("POLL >>>>>>") 
    Poll()
    cycle_number=cycle_number+1
    print("\r\n\r\n")
    time.sleep(3)                    
 
