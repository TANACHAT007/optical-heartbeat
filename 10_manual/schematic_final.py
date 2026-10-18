# Schematic of the BACKUP circuit (schemdraw symbols)
import schemdraw, schemdraw.elements as e
from schemdraw import Drawing
D = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
FS = 11
d = Drawing(unit=3); d.config(fontsize=FS, font='Thonburi')
# --- phototransistor receiver
d += e.Vdd().at((0, 3.0)).label('+5V')
d += e.Line().down(0.4)
d += (PT := e.NpnPhoto().anchor('collector').right().label('Q_PT\nphototransistor 940nm\n(ขายาว = collector)', 'left', ofst=(-0.1, 0)))
d += e.Line().at(PT.emitter).down(0.8)
d += e.Dot(); nP = d.here
d += e.Label().at((nP[0] - 1.1, nP[1] - 0.2)).label('NPT', fontsize=FS)
d += e.Resistor().down().label('R100k\n(โหลด PT)', 'left')
d += e.Ground()
# --- LM358 voltage follower
d += e.Line().at(nP).right(1.6); d += e.Dot(); nQ = d.here
d += e.Capacitor().down().label('C470nF (กรองไฟบ้าน)', 'right', ofst=(0.15, -1.0)); d += e.Ground()
d += e.Line().at(nQ).right(7.0)
U1 = e.Opamp(sign=True).anchor('in2').right(); d += U1
d += e.Label().at(U1.center).label('U1', fontsize=FS)
def pn(pt, n, dx, dy): d.add(e.Label().at((pt[0] + dx, pt[1] + dy)).label(f'ขา{n}', fontsize=9, color='#c60'))
pn(U1.in1, 2, -0.5, 0.25); pn(U1.in2, 3, -0.5, -0.25); pn(U1.out, 1, 0.1, 0.3)
d += e.Line().at(U1.in1).left(0.8); d += e.Dot(); nB = d.here
d += e.Resistor().left().label('R2.4k', 'top')
d += e.Capacitor(polar=True).left().label('C100µF (+ ฝั่ง R2.4k)', 'top', ofst=(0, .15))
d += e.Ground()
d += e.Line().at(U1.out).right(0.8); d += e.Dot(); JB = d.here
yb = nB[1] + 1.8
d += e.Line().at(JB).up(1.8)
d += e.ResistorVar().at((JB[0], yb)).left().tox(nB[0]).label('VR 100k (ปรับ gain)', 'top')
d += e.Line().down().toy(nB[1]).dot()
d += e.Line().at(JB).right(0.8)
d += e.Dot(open=True).label('ไป Arduino A0', 'right')
d += e.Label().at((U1.center[0] + 0.3, U1.center[1] - 3.0)).label('LM358: ขา8 = +5V · ขา4 = GND\nDC ×1 · AC ขยาย = 1 + VR/2.4k (ผ่าน C100µF) · op-amp ตัวที่สอง: ขา6-7 ผูกกัน ขา5 ลง GND', fontsize=9, color='#c60')
d.save(D + 'schematic_final_sheet1.png', dpi=130)
# --- IR driver
d = Drawing(unit=3); d.config(fontsize=FS, font='Thonburi')
d += e.Vdd().at((0, 5)).label('+5V')
d += e.Resistor().down().label('R220 Ω\n(R100 ถ้าแสงอ่อน)', 'right', ofst=(0.1, -0.2))
d += e.LED().down().label('IR LED 940nm', 'right')
d += e.Line().down(0.3)
d += (Q1 := e.BjtNpn().anchor('collector').right().label('Q1\nBC548', 'right', ofst=(0.1, 0)))
d += e.Ground().at(Q1.emitter)
d += e.Resistor().at(Q1.base).left().label('R1k', 'top'); d += e.Dot(open=True).label('Arduino D9', 'left')
d += e.Label().at((-1.0, 6.2)).label('วงจรส่งแสงอินฟราเรด: R220 ให้ ~17 mA (R100 ให้ ~35 mA)', fontsize=12)
d.save(D + 'schematic_final_sheet2.png', dpi=130)
print('ok')
