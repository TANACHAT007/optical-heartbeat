// Test: D9 and the on-board LED (D13) go HIGH together for 3 s, then LOW for 3 s.
void setup(){pinMode(9,OUTPUT);pinMode(LED_BUILTIN,OUTPUT);Serial.begin(115200);}
void loop(){
  digitalWrite(9,HIGH);digitalWrite(LED_BUILTIN,HIGH);Serial.println(F("D9=HIGH (should read ~5V)"));delay(3000);
  digitalWrite(9,LOW);digitalWrite(LED_BUILTIN,LOW);Serial.println(F("D9=LOW  (should read 0V)"));delay(3000);
}
