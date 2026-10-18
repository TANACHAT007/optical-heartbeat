// Arduino as a simple voltmeter: touch the wire on A0 to any point of the breadboard (A0 is a probe, GND must be shared).
// Prints the voltage on A0 5x per second (0-5 V, 5 V reference). D9 is driven HIGH so the IR LED is on.
void setup() { pinMode(9, OUTPUT); digitalWrite(9, HIGH); Serial.begin(115200); delay(1500); Serial.println(F("PROBE: touch the A0 wire on a point; V = voltage vs GND")); }
void loop() {
  long s = 0; for (uint8_t i = 0; i < 32; i++) { s += analogRead(A0); delayMicroseconds(200); }
  float v = (s / 32.0) * 5.0 / 1023.0;
  Serial.print(F("A0 = ")); Serial.print(v, 2); Serial.print(F(" V   "));
  if (v < 0.08) Serial.println(F("(GND / 0 V)")); else if (v > 4.8) Serial.println(F("(5 V)")); else Serial.println();
  delay(200);
}
