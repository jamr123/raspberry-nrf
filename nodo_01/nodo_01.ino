#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);
char receivedMessage[4];;
String stringMessage = "";
float response [2];
float numRadio = 2;
float data = 200;

long randNumber = 0;
bool newData = false;

const uint64_t TX0 = 0xAAAAAAAA01LL;
const uint64_t RX0 = 0xAAAAAAAAF1LL;
void setup(void)
{
  while (!Serial);
  Serial.begin(9600);
  printf_begin();
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  radio.openWritingPipe(TX0);
  radio.openReadingPipe(0, RX0);
  radio.setDataRate( RF24_1MBPS );
  radio.setAutoAck(1);
  radio.enableAckPayload();
  radio.enableDynamicPayloads();
  radio.setRetries(15, 15);
  radio.setChannel(0x20);
  radio.setCRCLength(RF24_CRC_16);
  radio.printDetails();
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
    stringMessage = String(receivedMessage);
    stringMessage =stringMessage.substring(0, 4);
    newData = true;
  }
}

void showData() {
  if (newData == true) {
    
    if (stringMessage == "SYNC") {
      randNumber = random(0, 5000);
      Serial.println(randNumber);
      delayMicroseconds(randNumber);
    }
    if (stringMessage == "POLL") {
       randNumber = random(0, 5000);
       Serial.println(randNumber);
       sendPool();
    }

    stringMessage = "";
    newData = false;
  }
}

void sendPool() {

  radio.stopListening();

  response[0] = numRadio;
  response[1] = data;
  radio.write(response, sizeof(response));

  radio.startListening();

}




int serial_putc( char c, FILE * )
{
  Serial.write( c );

  return c;
}

void printf_begin(void)
{
  fdevopen( &serial_putc, 0 );
}
