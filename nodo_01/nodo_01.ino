#include<SPI.h>
#include<RF24.h>
RF24 radio(9, 10);
char receivedMessage[16] = {0};
String stringMessage = "";
bool newData = false;

const uint64_t TX = 0xAAAAAAAA01LL;
const uint64_t RX = 0xAAAAAAAAFFLL;
void setup(void)
{
  while (!Serial);
  Serial.begin(9600);
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  radio.setChannel(0x70);
  radio.openWritingPipe(TX);
  radio.openReadingPipe(0, RX);
  radio.setDataRate( RF24_1MBPS );
  radio.setAutoAck(1);
  radio.enableAckPayload();
  radio.enableDynamicPayloads();
  radio.startListening();
  Serial.println("inicio");
}

void loop(void)
{
    
  
 getData();
 showData();

}


void getData() {
  if ( radio.available() ) {
    radio.read( &receivedMessage, sizeof(receivedMessage) );
    stringMessage = String(receivedMessage[0]);
 
  }
}

void showData() {
  if (newData == true) {
    Serial.println(stringMessage);
    stringMessage="";
    newData = false;
  }
}
