#define BOUTTON1 3
#define BOUTTON2 4

void setup() {
  // on configure les broches en entrée avec une résistance de pull-up
  pinMode(BOUTTON1, INPUT_PULLUP); 
  pinMode(BOUTTON2, INPUT_PULLUP); 
  Serial.begin(9600); 
}

void loop() {
  // on lit l'état des boutons
  int etatBouton1 = digitalRead(BOUTTON1); 
  int etatBouton2 = digitalRead(BOUTTON2); 

// si un des boutons est appuyé, on envoie un message sur le port série qui executera une des requêtes HTTP corepondante
  if (etatBouton1 == LOW) {
    Serial.println("1"); 
  } 
  else if (etatBouton2 == LOW) {
    Serial.println("2"); 
  } 

  delay(500); 
}
