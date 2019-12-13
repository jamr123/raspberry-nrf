#include<SPI.h>
#include<RF24.h>
RF24 radio(9, 10);  
char receivedMessage[16] = {0}; 
void setup(void)
{
  while(!Serial);                                 
  Serial.begin(9600);
  radio.begin();                                 
  radio.setPALevel(RF24_PA_MAX);                 
  radio.setChannel(0x70);
  radio.openWritingPipe(0xAAAAAAAA01LL);         // this pipe is to send the data to RPI, different arduino nodes will have different writing pipe numbers,
                                                 // such as, 1, 2,  ...
                                                 // the first arduino the node # is 1, 2nd arduino the node # will be 2, and so on
                                                 
  const uint64_t pipe = (0xAAAAAAAAFFLL);        // this pipe is to listen the syn signal from RPI    
  radio.openReadingPipe(1, pipe);                 
  radio.enableDynamicPayloads();                  
  radio.powerUp();  
  radio.startListening();                         
}

void loop(void)
{  
   radio.startListening();    
   if(radio.available())  
   {
       radio.read(receivedMessage, sizeof(receivedMessage));          
       String stringMessage(receivedMessage);      // does not need to be a String, please use whatever, as long as, it can detect the syn signal from Raspberry Pi    
       if(stringMessage == "A")                    // this step confirm arduino recieve the syn signal from RPI, A can be 99
       {  
           // let me assume these things are below, please create the codes
           // generate a random number which is in between for example 1 and 50,000
           // save it to 'rn" 
           // delayMicroseconds(rn); 
        }    

        if(stringMessage == "B")                         // this step confirm arduino recieve the poll signal from RPI, B can be 01, 02, please use good working ones
                                                         // to make sure arduino can detect the coding from Raspberry pi
       {  
          radio.stopListening();                         // radio must be stop, otherwise, it can not write
          radio.write( char_array, sizeof(char_array) ); // send the data "rn" back to RPI, you shall revise this line to make sure Arduino is able to send a numerical data back to RPI 
          
          // Serial.println to print out the "rn" so i can check if RPI receive the same data
                                    
       }
    }            
}

}
