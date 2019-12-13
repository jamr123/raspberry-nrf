#include<SPI.h>                   // spi library for connecting nrf
#include <Wire.h>                             // i2c libary fro 16x2 lcd display
#include<RF24.h>                  // nrf library
#include <LiquidCrystal_I2C.h>     // 16x2 lcd display library

LiquidCrystal_I2C lcd(0x27, 16, 2);         // i2c address is 0x27

RF24 radio(9, 10) ;  // ce, csn pins    
void setup(void) {
  while (!Serial) ;
  Serial.begin(9600) ;     // start serial monitor baud rate
  Serial.println("Starting.. Setting Up.. Radio on..") ; // debug message
  radio.begin();        // start radio at ce csn pin 9 and 10
  radio.setPALevel(RF24_PA_MAX) ;   // set power level
  radio.setChannel(0x64) ;            // set chanel at 76
  const uint64_t pipe = 0xE0E0F1F1E0LL ;    // pipe address same as sender i.e. raspberry pi
  radio.openReadingPipe(1, pipe) ;        // start reading pipe 
  radio.enableDynamicPayloads() ;
  radio.powerUp() ;          
  Wire.begin();                 //start i2c address
  lcd.begin();                    // start lcd 
  lcd.home();                       
  lcd.print("Ready to Receive");  // print starting message on lcd 
  delay(2000);
  lcd.clear();
}

void loop(void) {

  radio.startListening() ;        // start listening forever
  char receivedMessage[32] = {0} ;   // set incmng message for 32 bytes
  if (radio.available()) {       // check if message is coming
    radio.read(receivedMessage, sizeof(receivedMessage));    // read the message and save
    Serial.println(receivedMessage) ;    // print message on serial monitor 
    Serial.println("Turning off the radio.") ;   // print message on serial monitor
    radio.stopListening() ;   // stop listening radio
    String stringMessage(receivedMessage) ;     // change char to string
    lcd.clear();    // clear screen for new message
    delay(1000);    // delay of 1 second 
    lcd.print(stringMessage);   // print received mesage
  }
  delay(10);
}
