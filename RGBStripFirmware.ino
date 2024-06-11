#include <SoftwareSerial.h>

//#define DEBUG
#define RED_PIN 5
#define GREEN_PIN 6
#define BLUE_PIN 9

// SoftwareSerial bluetooth(3, 2);

void setup() {
  // bluetooth.begin(115200);
  Serial.begin(2000000);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  // strip test
  setColor(0x88, 0x88, 0x88);
  delay(50);
  setColor(0, 0, 0);
}

void setColor(uint8_t r, uint8_t g, uint8_t b) {
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

uint8_t color[3];
void loop() {
  if (Serial.available() > 0) {
    Serial.readBytes(color, 3);
    setColor(color[0], color[1], color[2]);
  }
}
