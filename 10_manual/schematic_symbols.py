# Proper schematic (symbols) with schemdraw. Sheet 1 = analog front end, sheet 2 = power/Vref + drivers + OLED.
import schemdraw, schemdraw.elements as e
from schemdraw import Drawing
import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc')
plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
D = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
FS = 11

# ================= sheet 1 (simple: one op-amp) =================
d = Drawing(unit=3); d.config(fontsize=FS, font='Thonburi')
d += e.Vdd().at((-1, 3.0)).label('+5V')
d += e.Line().down(0.4)
d += (PT := e.NpnPhoto().anchor('collector').right().label('Q_PT\nphototransistor 940nm\n(ขายาว = collector)', 'left', ofst=(-0.1, 0)))
d += e.Line().at(PT.emitter).down(0.8)
d += e.Dot(); nP = d.here
d += e.Label().at((nP[0] - 1.1, nP[1] - 0.2)).label('NPT', fontsize=FS)
d += e.Resistor().down().label('R10k\n(โหลด PT)', 'left')
d += e.Ground()
d += e.Line().at(nP).right(0.6)
d += e.Capacitor(polar=True).right().reverse().label('10µF (ตัด DC)\nขา + ด้านขวา (ฝั่ง X)', 'top', ofst=(0, .15))
d += e.Dot().label('X', 'top', ofst=(0, .3)); nX = d.here
d += e.Resistor().down().label('R100k\n(ไบอัส)', 'left')
d += e.Line().down(0.4); d += e.Dot(open=True).label('Vref', 'right')
d += e.Line().at(nX).right(0.8)
U1 = e.Opamp(sign=True).anchor('in2').right(); d += U1
d += e.Label().at(U1.center).label('U1', fontsize=FS)
def pn(pt, n, dx, dy): d.add(e.Label().at((pt[0] + dx, pt[1] + dy)).label(f'ขา{n}', fontsize=9, color='#c60'))
pn(U1.in1, 2, -0.5, 0.25); pn(U1.in2, 3, -0.5, -0.25); pn(U1.out, 1, 0.1, 0.3)
d += e.Line().at(U1.in1).left(0.9); d += e.Dot().label('FB', 'left', ofst=(0, .2)); nB = d.here
d += e.Resistor().up().label('R2.4k', 'left'); d += e.Line().up(0.4); d += e.Dot(open=True).label('Vref', 'top')
d += e.Line().at(U1.out).right(0.8); d += e.Dot(); JB = d.here
yb = nB[1] + 1.8
d += e.Line().at(JB).up(4.0)
d += e.ResistorVar().at((JB[0], yb)).left().tox(nB[0] - 0.9).label('VR 100k\n(หมุนปรับ gain)', 'top')
xb = nB[0] - 0.9
d += e.Line().down().toy(nB[1]).dot(); d += e.Line().right().tox(nB[0])
d += e.Capacitor().at((JB[0], nB[1] + 4.0)).left().tox(xb).label('Cf 10nF', 'top')
d += e.Line().down().toy(yb).dot()
d += e.Line().at(JB).right(0.6); d += e.Dot().label('OUT', 'bottom', ofst=(0, -.1))
d += e.Resistor().right().label('R100k (LPF)', 'top')
d += e.Dot().label('Y', 'top', ofst=(0, .3)); nY = d.here
d += e.Capacitor().down().label('470nF', 'left'); d += e.Ground()
d += e.Line().at(nY).right(1.5).dot(open=True).label('ไป Arduino A0', 'right')
d += e.Label().at((U1.center[0] + 1.6, U1.center[1] - 2.2)).label('LM358: ขา8 = +5V · ขา4 = GND (+C100nF)\nแอมป์ตัวที่สอง: ขา6 ต่อขา7 และขา5 ต่อ Vref (ไม่ใช้งาน)', fontsize=9, color='#c60')
d.save(D + 'schematic_sheet1.png', dpi=130)

# ================= sheet 2 =================
d = Drawing(unit=3); d.config(fontsize=FS, font='Thonburi')
# power + Vref
d += e.Vdd().at((0, 5)).label('+5V')
d += e.Resistor().down().label('R10k', 'right', ofst=(0.1, -0.2))
d += e.Dot().label('Vref = 2.5V', 'right', ofst=(0.1, 0)); nV = d.here
d += e.Resistor().down().label('R10k', 'right'); d += e.Ground()
d += e.Line().at(nV).left(1.6); d += e.Capacitor(polar=True).down().label('10µF', 'left'); d += e.Ground()
d += e.Label().at((-0.2, 6.2)).label('1) ไฟ + Vref', fontsize=13)
# decoupling
d += e.Vdd().at((5, 5)).label('+5V')
d += e.Line().down(0.4); d += e.Dot(); nP = d.here
d += e.Capacitor(polar=True).down().label('100µF', 'right'); d += e.Ground()
d += e.Line().at(nP).left(1.4); d += e.Capacitor().down().label('100nF', 'left'); d += e.Ground()
d += e.Label().at((4.6, 6.2)).label('ตัวกรองไฟ (ใกล้ LM358)', fontsize=11)
# IR driver
x0 = 10
d += e.Vdd().at((x0, 5)).label('+5V')
d += e.Resistor().down().label('R220', 'right', ofst=(0.1, -0.2))
d += e.LED().down().label('IR LED 940nm', 'right')
d += e.Line().down(0.3)
d += (Q1 := e.BjtNpn().anchor('collector').right().label('Q1\nBC548', 'right', ofst=(0.1, 0)))
d += e.Ground().at(Q1.emitter)
d += e.Resistor().at(Q1.base).left().label('R1k', 'top'); d += e.Dot(open=True).label('Arduino D9', 'left')
d += e.Label().at((x0 - 0.2, 6.2)).label('2) ส่งแสงอินฟราเรด', fontsize=13)
d += e.Label().at((17.2, 5.2)).label('LED บอกชีพจร = LED ที่ติดมากับบอร์ด Arduino (ขา D13)\nไม่ต้องต่ออะไรเพิ่ม', fontsize=11)
# OLED
x2 = 24
d += (OL := e.Ic(pins=[e.IcPin(name='GND', side='left'), e.IcPin(name='VCC', side='left'), e.IcPin(name='SCL', side='left'), e.IcPin(name='SDA', side='left')], size=(2.6, 3), lblsize=11, label='OLED\n0.96" I2C\n0x3C').theta(0).at((x2, 2.5)))
d += e.Line().at(OL.GND).left(0.5); d += e.Ground()
d += e.Line().at(OL.VCC).left(0.5); d += e.Vdd().label('+5V')
d += e.Line().at(OL.SCL).left(0.8); d += e.Dot(open=True).label('Arduino D3', 'left')
d += e.Line().at(OL.SDA).left(0.8); d += e.Dot(open=True).label('Arduino D2', 'left')
d += e.Label().at((x2, 6.2)).label('4) จอ OLED', fontsize=13)
d.save(D + 'schematic_sheet2.png', dpi=130)
print('ok')
