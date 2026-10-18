// Optical Heartbeat Detector — BACKUP (simplest circuit)
//   IR LED -> finger -> phototransistor -> load R -> LM358 voltage follower -> R1k -> A0 (C100nF to GND)
//   D9 -> R1k -> Q1 BC548 base (switches the IR LED, always on)
// No Vref divider, no coupling capacitor, no gain stage: the DC part is removed in software.
// Serial 115200:  "BPM,<value>" per beat
//   'p' toggles raw plot mode  (filtered, +threshold, -threshold)
//   'd' toggles DC print       ("DC,<counts>,<volts>" once per second: use it to tune the load resistor)

#if defined(__AVR_ATmega32U4__)
  #define ADC_REF INTERNAL          // Leonardo: 2.56 V reference -> 2.5 mV per count
  const float ADC_VMAX = 2.56f;
#else
  #define ADC_REF DEFAULT           // UNO: 5 V reference
  const float ADC_VMAX = 5.0f;
#endif

const uint8_t PIN_SIG = A0;
const uint8_t PIN_IR = 9;
const uint8_t PIN_BEAT = LED_BUILTIN;

const uint16_t SAMPLE_MS = 20;       // one mains cycle (50 Hz): every sample is a mean over 20 ms -> hum cancelled
const uint16_t REFRACTORY_MS = 300;  // max 200 BPM
const uint16_t TIMEOUT_MS = 4000;    // no beat -> finger off
const float MIN_THR = 0.4f;          // counts: averaged samples are very quiet
const uint8_t AVG_N = 5;

float baseline = 0, lowpass = 0, level = 0;
bool baseInit = false, above = false, plotMode = false, dcMode = false;
unsigned long lastBeat = 0, beatLedOff = 0, lastDc = 0;
float bpmBuf[AVG_N];
uint8_t bpmCount = 0, bpmIdx = 0;

void setup() {
  analogReference(ADC_REF);
  pinMode(PIN_IR, OUTPUT);
  pinMode(PIN_BEAT, OUTPUT);
  digitalWrite(PIN_IR, HIGH);
  Serial.begin(115200);
  analogRead(PIN_SIG);               // first read after changing the reference is unreliable
  Serial.println(F("Backup heartbeat detector ready. Rest your finger lightly on the sensor."));
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'p') plotMode = !plotMode;
    if (c == 'd') dcMode = !dcMode;
  }

  long sum = 0; uint16_t n = 0;
  unsigned long t0 = micros();
  while (micros() - t0 < (unsigned long)SAMPLE_MS * 1000UL) { sum += analogRead(PIN_SIG); n++; }
  unsigned long now = millis();
  float raw = (float)sum / n;

  if (!baseInit) { baseline = raw; baseInit = true; }
  baseline += (raw - baseline) * 0.04f;            // slow DC tracker (about 0.5 s)
  float ac = raw - baseline;
  lowpass += (ac - lowpass) * 0.5f;                // light smoothing
  level = max(fabs(lowpass), level * 0.99f);       // decaying amplitude
  float thr = max(level * 0.5f, MIN_THR);

  if (dcMode && now - lastDc > 1000) {
    lastDc = now;
    Serial.print(F("DC,")); Serial.print(raw, 1); Serial.print(','); Serial.println(raw * ADC_VMAX / 1023.0f, 3);
  }
  if (plotMode) {
    Serial.print(lowpass); Serial.print(','); Serial.print(thr); Serial.print(','); Serial.println(-thr);
  }

  if (!above && lowpass > thr && now - lastBeat > REFRACTORY_MS) {
    above = true;
    if (lastBeat != 0) {
      float bpm = 60000.0f / (now - lastBeat);
      if (bpm >= 40 && bpm <= 200) {
        bpmBuf[bpmIdx] = bpm;
        bpmIdx = (bpmIdx + 1) % AVG_N;
        if (bpmCount < AVG_N) bpmCount++;
        float s = 0;
        for (uint8_t i = 0; i < bpmCount; i++) s += bpmBuf[i];
        if (!plotMode && !dcMode) { Serial.print(F("BPM,")); Serial.println(s / bpmCount, 0); }
      }
    }
    lastBeat = now;
    digitalWrite(PIN_BEAT, HIGH);
    beatLedOff = now + 80;
  } else if (above && lowpass < thr * 0.3f) {
    above = false;
  }

  if (beatLedOff && now > beatLedOff) { digitalWrite(PIN_BEAT, LOW); beatLedOff = 0; }

  if (lastBeat && now - lastBeat > TIMEOUT_MS) {
    bpmCount = 0; bpmIdx = 0; lastBeat = 0;
    if (!plotMode && !dcMode) Serial.println(F("No pulse (finger off?)"));
  }
}
