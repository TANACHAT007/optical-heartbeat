# Optical Heartbeat Detector — วงจรแบบง่าย (v2, 2026-10-17, ยังไม่ได้ทดสอบกับของจริง)

ไฟ 5V จาก USB เท่านั้น · Vref = 2.5V · ใช้ op-amp แค่ 1 ตัว (LM358 ตัวเดียว ใช้ครึ่งเดียว)

## สายสัญญาณ
IR LED (Q1 สวิตช์) → นิ้ว → Phototransistor → R10k (โหลด) → C10µF (ตัด DC) → LM358 ขยาย (VR ปรับ gain) → R100k + C470nF (กรอง) → **A0**
LED บอกชีพจร = LED บนบอร์ด Arduino (D13) ไม่ต้องต่อ

## ตำแหน่งบน breadboard (คอลัมน์+แถว) ดูรูป step1–7.png / fritzing_style.png
| ส่วน | ต่อ |
|---|---|
| ไฟ | Arduino 5V → แถบ 5V · GND → แถบ GND · C100µF, C100nF คร่อม 5V/GND |
| Vref | R10k 5V→Vref, R10k Vref→GND, C10µF Vref→GND (แถบ Vref) |
| LM358 | คร่อมร่องกลาง ขา1 ที่ 24f · ขา8→5V · ขา4→GND · ตัวที่ไม่ใช้: ขา6 ต่อขา7, ขา5 ต่อ Vref |
| รับแสง | PT ขายาว→5V · ขาสั้น→จุด NPT · R10k จาก NPT ลง GND |
| ตัด DC + ไบอัส | C10µF (ขา + ที่ฝั่ง X, ขา − ที่ NPT) → จุด X → ขา3 · R100k จาก X ไป Vref |
| ขยาย | ขา2 → R2.4k → Vref · VR100k + C10nF คร่อมขา1–ขา2 |
| กรอง | ขา1 → R100k → Y → C470nF → GND · Y → A0 |
| IR LED | 5V → R220 → IR LED(A→K) → Q1 collector · Q1 emitter→GND · D9 → R1k → Q1 base |
| จอ OLED (เลือกต่อ) | GND, VCC→5V, SDA→D2, SCL→D3 (Leonardo) |

## อุปกรณ์ที่ใช้
LM358×1 · BC548×1 · IR LED×1 · Phototransistor×1 · R220×1 · R1k×1 · R2.4k×1 · R10k×3 · R100k×2 · VR100k×1 · C10nF×1 · C100nF×1 · C470nF×1 · C10µF×2 · C100µF×1

## จูนครั้งแรก
1. Serial Monitor 115200 · ส่ง `p` เพื่อดูคลื่นใน Serial Plotter
2. วางนิ้วเบา ๆ รอ 5–6 วินาที (HPF ต้องนิ่ง) หมุน VR ให้คลื่นสูง ~50–300 count ไม่ชนขอบ 0/1023
3. A0 ติดเพดาน/แบน: ลด gain หรือเพิ่ม R220 (ลดแสง) หรือกันแสงรอบข้าง

## ผลจำลอง (ngspice, โมเดล op-amp แบบง่าย — ดู 10_manual/simulation.png)
กระแสแสงนิ่ง 30 µA → ~36 count · 100 µA → ~87 count (VR 100k) · เกิน ~500 µA ที่ PT อิ่มตัว

## ข้อจำกัดที่ยังไม่ยืนยัน
- ยังไม่ได้ต่อจริง กระแสจริงของ PT ตอนแตะนิ้วไม่ได้วัด
- เคสสมมติ breadboard 85×55 mm
- โจทย์ห้ามโมดูลสำเร็จรูป: จอ OLED ต้องถามอาจารย์ก่อน
