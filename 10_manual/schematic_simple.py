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
d += e.Resistor().down().label('R10k\n(โหลด PT)', 'left')
d += e.Ground()
# --- LM358 voltage follower
d += e.Line().at(nP).right(2.0)
U1 = e.Opamp(sign=True).anchor('in2').right(); d += U1
d += e.Label().at(U1.center).label('U1', fontsize=FS)
def pn(pt, n, dx, dy): d.add(e.Label().at((pt[0] + dx, pt[1] + dy)).label(f'ขา{n}', fontsize=9, color='#c60'))
pn(U1.in1, 2, -0.5, 0.25); pn(U1.in2, 3, -0.5, -0.25); pn(U1.out, 1, 0.1, 0.3)
d += e.Line().at(U1.in1).left(0.7); jx = d.here
d += e.Line().up(1.9); d += e.Line().right().tox(U1.out[0] + 0.8)
d += e.Line().down().toy(U1.out[1]).dot()
d += e.Line().at(U1.out).right(0.8)
d += e.Dot(open=True).label('ไป Arduino A0', 'right')
d += e.Label().at((U1.center[0] + 0.3, U1.center[1] - 2.2)).label('LM358: ขา8 = +5V · ขา4 = GND\nขา 1 ต่อขา 2 (บัฟเฟอร์) · op-amp ตัวที่สอง: ขา6-7 ผูกกัน ขา5 ลง GND', fontsize=9, color='#c60')
d.save(D + 'schematic_simple_sheet1.png', dpi=130)
# --- IR driver
d = Drawing(unit=3); d.config(fontsize=FS, font='Thonburi')
d += e.Vdd().at((0, 5)).label('+5V')
d += e.Resistor().down().label('R220', 'right', ofst=(0.1, -0.2))
d += e.LED().down().label('IR LED 940nm', 'right')
d += e.Line().down(0.3)
d += (Q1 := e.BjtNpn().anchor('collector').right().label('Q1\nBC548', 'right', ofst=(0.1, 0)))
d += e.Ground().at(Q1.emitter)
d += e.Resistor().at(Q1.base).left().label('R1k', 'top'); d += e.Dot(open=True).label('Arduino D9', 'left')
d += e.Label().at((-1.0, 6.2)).label('วงจรส่งแสงอินฟราเรด (เหมือนแบบเดิม)', fontsize=12)
d.save(D + 'schematic_simple_sheet2.png', dpi=130)
print('ok')
