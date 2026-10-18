// Optical Heartbeat Detector — BACKUP circuit, Arduino UNO / Leonardo, optional OLED
//   OLED 0.96" SSD1306 I2C @0x3C: SDA=A4, SCL=A5 on UNO (D2/D3 on Leonardo), VCC=5V, GND. Runs without it.
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
  #define ADC_REF DEFAULT           // UNO: 5 V reference (INTERNAL would be only 1.1 V and clip the 1-2 V DC level)
  const float ADC_VMAX = 5.0f;
#endif

// IR LED driver transistor: 1 = BC558 (PNP, D9 LOW turns the LED on), 0 = BC548 (NPN, D9 HIGH turns it on)
#define PNP_DRIVER 0
const uint8_t IR_ON = PNP_DRIVER ? LOW : HIGH;

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 oled(128, 64, &Wire, -1);
bool oledOk = false;

void showBpm(float bpm, bool pulse) {
  if (!oledOk) return;
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.print(F("Heart rate"));
  if (pulse) oled.fillCircle(120, 4, 4, SSD1306_WHITE);
  oled.setTextSize(4);
  oled.setCursor(0, 22);
  if (bpm > 0) oled.print((int)(bpm + 0.5f)); else oled.print(F("--"));
  oled.setTextSize(2);
  oled.setCursor(92, 42);
  oled.print(F("BPM"));
  oled.display();
}

const uint8_t PIN_SIG = A0;
const uint8_t PIN_IR = 9;
const uint8_t PIN_BEAT = LED_BUILTIN;

const uint16_t SAMPLE_MS = 20;       // one mains cycle (50 Hz): every sample is a mean over 20 ms -> hum cancelled
const uint16_t REFRACTORY_MS = 300;  // max 200 BPM
const uint16_t TIMEOUT_MS = 4000;    // no beat -> finger off
const float MIN_THR = 0.4f * 2.56f / ADC_VMAX;   // counts: averaged samples are very quiet (0.4 at 2.56 V ref)
const uint8_t AVG_N = 5;

float baseline = 0, lowpass = 0, level = 0;
bool baseInit = false, above = false, plotMode = false, dcMode = false;
unsigned long lastBeat = 0, beatLedOff = 0, lastDc = 0;
float bpmBuf[AVG_N], shownBpm = 0;
uint8_t bpmCount = 0, bpmIdx = 0;

void setup() {
  analogReference(ADC_REF);
  pinMode(PIN_IR, OUTPUT);
  pinMode(PIN_BEAT, OUTPUT);
  digitalWrite(PIN_IR, IR_ON);
  Serial.begin(115200);
  Wire.begin();
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  showBpm(0, false);
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
        shownBpm = s / bpmCount;
        if (!plotMode && !dcMode) { Serial.print(F("BPM,")); Serial.println(shownBpm, 0); }
      }
    }
    lastBeat = now;
    digitalWrite(PIN_BEAT, HIGH);
    beatLedOff = now + 80;
    showBpm(shownBpm, true);
  } else if (above && lowpass < thr * 0.3f) {
    above = false;
  }

  if (beatLedOff && now > beatLedOff) { digitalWrite(PIN_BEAT, LOW); beatLedOff = 0; showBpm(shownBpm, false); }

  if (lastBeat && now - lastBeat > TIMEOUT_MS) {
    bpmCount = 0; bpmIdx = 0; lastBeat = 0; shownBpm = 0;
    showBpm(0, false);
    if (!plotMode && !dcMode) Serial.println(F("No pulse (finger off?)"));
  }
}
