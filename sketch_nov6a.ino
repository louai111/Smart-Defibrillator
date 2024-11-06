int bit7Pin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(bit7Pin, INPUT);

}

void loop() {
  int bit7 = digitalRead(bit7Pin);

  if (bit7 = HIGH) {
  Serial.println("HIGH") ;
  }

  delay(1000);
}
