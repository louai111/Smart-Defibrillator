#include "DHT.h"
#include "MAX30100_PulseOximeter.h"

// Pin Definitions
const int buttonPin = 8;   
const int batteryPin = A0; 
const int capChargePin = 2;
const int capTestPin = 3;
const int batTestPin = 4; 
const int capReadPin = A7;
const int relayPin = 7;
const int pushButtonOut = 9;

uint32_t tsLastPoxReport = 0;
#define POX_PERIOD_MS     1000

const float voltageDividerRatio = 2.0;  
const float batteryThreshold = 7.5; 
const float capTargetVoltage = 4.0; 
const unsigned long timeOut = 5000; 
unsigned long chargeTime = 0;

float batteryVoltage = 0;

#define DHTPIN 10
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
PulseOximeter pox;

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(capChargePin, OUTPUT);
  pinMode(batTestPin, OUTPUT);
  pinMode(capTestPin, OUTPUT);
  pinMode(pushButtonOut, OUTPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(pushButtonOut, HIGH);
  digitalWrite(relayPin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(buttonPin) == HIGH) {
    batteryTest();
    delay(100);
    capacitorChargeTest();
    Serial.print(batteryVoltage);
    Serial.print("_");
    Serial.println(chargeTime);
  }
  delay(100);
  Serial.println(dht.readTemperature());
  pox.update();
  if (millis() - tsLastPoxReport > POX_PERIOD_MS) {
    float bpm = pox.getHeartRate();
    tsLastPoxReport = millis();
    if (bpm == 0) {
      Serial.println("1");
      digitalWrite(relayPin, HIGH);
      delay(2000);
      digitalWrite(relayPin, LOW);
    }
  } 

}

// Battery Test Function
void batteryTest() {
  digitalWrite(batTestPin, HIGH);   
  delay(50);                    
  int batteryADC = analogRead(batteryPin);
  batteryVoltage = batteryADC * (5.0 / 1023.0) * voltageDividerRatio;
  // Serial.print("Battery Voltage: ");
  // Serial.println(batteryVoltage);

  if (batteryVoltage < batteryThreshold) {
    // Serial.println("Battery too low!");
  }
  digitalWrite(batTestPin, LOW);
}

// Capacitor Charge Time Test Function
void capacitorChargeTest() {
  digitalWrite(capTestPin, HIGH);
  delay(50);
  digitalWrite(capChargePin, HIGH); 
  unsigned long startTime = millis();
  chargeTime = 0;
  delay(20);
  
  while (analogRead(capReadPin) < (capTargetVoltage / 5.0 * 1023.0)) {
    chargeTime = millis() - startTime;
    Serial.println(1);
    if (chargeTime > timeOut) {
      // Serial.println("Charge timeout!");
      break;
    }
  }
  
  // digitalWrite(capChargePin, LOW);
  // digitalWrite(capTestPin, LOW);
  // Serial.print("Charge Time to 80%: ");
  // Serial.print(chargeTime);
  // Serial.println(" ms");
}