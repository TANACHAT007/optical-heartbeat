// Optical Heartbeat Detector — Arduino Leonardo / UNO
// A0  <- analog front end (LM358 U1 via RC low-pass, centred at ~2.5 V)
// D9  -> R1k -> Q1 BC548 base (switches the IR LED)
// LED_BUILTIN (D13) = heartbeat indicator, no external parts
// OLED 0.96" SSD1306 128x64 I2C @0x3C: SDA=D2, SCL=D3 (Leonardo), VCC=5V, GND
// Serial 115200: "BPM,<value>" per beat; send 'p' to toggle raw plot mode.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 oled(128, 64, &Wire, -1);
bool oledOk = false;
float shownBpm = 0;

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
const uint8_t PIN_BEAT = LED_BUILTIN;   // on-board LED (D13)

const uint16_t SAMPLE_MS = 20;       // 50 Hz sample rate = one mains cycle
const uint16_t REFRACTORY_MS = 300;  // max 200 BPM
const uint16_t TIMEOUT_MS = 3000;    // no beat -> finger off
const uint8_t AVG_N = 5;

float baseline = 512;
float level = 0;      // running peak-to-peak estimate
float lowpass = 0;
unsigned long lastBeat = 0, lastSample = 0, beatLedOff = 0;
float bpmBuf[AVG_N];
uint8_t bpmCount = 0, bpmIdx = 0;
bool plotMode = false;
bool above = false;

void setup() {
  pinMode(PIN_IR, OUTPUT);
  pinMode(PIN_BEAT, OUTPUT);
  digitalWrite(PIN_IR, HIGH);
  Serial.begin(115200);
  Wire.begin();
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  showBpm(0, false);
  Serial.println(F("Optical Heartbeat Detector ready. Place finger on sensor."));
}

void loop() {
  if (Serial.available() && Serial.read() == 'p') plotMode = !plotMode;

  // one sample = mean of ADC reads over exactly one 50 Hz mains cycle (20 ms): cancels mains hum
  long sum = 0; uint16_t n = 0;
  unsigned long t0 = micros();
  while (micros() - t0 < (unsigned long)SAMPLE_MS * 1000UL) { sum += analogRead(PIN_SIG); n++; }
  unsigned long now = millis();
  float raw = (float)sum / n;
  baseline += (raw - baseline) * 0.04;            // slow DC tracker
  float ac = raw - baseline;
  lowpass += (ac - lowpass) * 0.5;                // light smoothing
  level = max(fabs(lowpass), level * 0.99f);      // decaying amplitude

  float thr = max(level * 0.5f, 3.0f);            // ignore noise < ~3 counts
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
        float sum = 0;
        for (uint8_t i = 0; i < bpmCount; i++) sum += bpmBuf[i];
        shownBpm = sum / bpmCount;
        if (!plotMode) { Serial.print(F("BPM,")); Serial.println(shownBpm, 0); }
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
    if (!plotMode) Serial.println(F("No pulse (finger off?)"));
  }
}
