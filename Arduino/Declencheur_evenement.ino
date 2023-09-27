
#define BUT1 11

int etatboutton1;



void setup() {
  Serial.begin(9600);
  pinMode(BUT1, INPUT_PULLUP);

}

void loop() {
  etatboutton1 = digitalRead(BUT1);


  if (etatboutton1 == LOW ) {
 
    Serial.println("Envoi de la requête HTTP 1...");
    Serial.println("Envoi de la requête HTTP...");
    Serial.println("GET /recevoir?nom=120 HTTP/1.1");
    Serial.println("Host: localhost:8080");
    Serial.println("Connection: close");
    Serial.println();
    delay(1000); 
  }



  delay(100); 
}
