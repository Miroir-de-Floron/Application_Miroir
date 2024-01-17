#include "SPI.h"
#include "MFRC522.h"
#define RST_PIN  9 // RES pin
#define SS_PIN  10 // SDA (SS) pin

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
   Serial.begin(9600);
   SPI.begin();
   mfrc522.PCD_Init();
   delay(4);
}


void loop() {
   //on regarde si la carte et présente
   if ( ! mfrc522.PICC_IsNewCardPresent()) {
      return;
   }

   if ( ! mfrc522.PICC_ReadCardSerial()) {
      return;
   }
   
  int i;
  String id ="";
  for(i=0;i<10;++i){
   //on concatene l'id
    id += mfrc522.uid.uidByte[i];

}
//on print l'id
Serial.println(id);
delay(1000);

}