// Simple IR link test: D9 -> R1k -> Q1 (BC548) -> IR LED blinks; the phototransistor + R10k node goes DIRECTLY to A0.
// Prints: ON (LED on), OFF (LED off), DIFF = ON-OFF (ADC counts, 5 V reference = 4.9 mV/count).
//   DIFF > 20   -> the receiver sees the IR LED  (good)
//   DIFF < 3    -> receiver does not see the LED (check wiring/polarity/aim)
// 1 = BC558 (PNP: D9 LOW = LED on), 0 = BC548 (NPN: D9 HIGH = LED on)
#define PNP_DRIVER 1
const uint8_t IR_ON = PNP_DRIVER ? LOW : HIGH, IR_OFF = PNP_DRIVER ? HIGH : LOW;
void setup() {
  pinMode(9, OUTPUT);
  digitalWrite(9, IR_OFF);
  Serial.begin(115200);
  delay(1500);
  Serial.println(F("IR test: A0 = phototransistor emitter node (NPT). Aim the IR LED at the phototransistor."));
}
float avg(uint8_t n) { long s = 0; for (uint8_t i = 0; i < n; i++) { s += analogRead(A0); delayMicroseconds(300); } return (float)s / n; }
void loop() {
  digitalWrite(9, IR_OFF);  delay(250); float off = avg(64);
  digitalWrite(9, IR_ON); delay(250); float on = avg(64);
  float diff = on - off;
  Serial.print(F("OFF=")); Serial.print(off, 1);
  Serial.print(F("  ON=")); Serial.print(on, 1);
  Serial.print(F("  DIFF=")); Serial.print(diff, 1);
  Serial.print(F("  (")); Serial.print(diff * 5.0 / 1023.0, 3); Serial.print(F(" V)  "));
  Serial.println(diff > 20 ? F("IR OK") : (diff > 3 ? F("weak") : F("no IR seen")));
}
