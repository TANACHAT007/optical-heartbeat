# Block + connection diagram of the finished circuit (matplotlib). Values match 08_firmware/README_wiring.md
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc') if False else None
for f in ('/System/Library/Fonts/Supplemental/Thonburi.ttc',): fm.fontManager.addfont(f)
plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
from matplotlib.patches import FancyBboxPatch, Circle

OUT = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/circuit_diagram.png'
fig, ax = plt.subplots(figsize=(16, 9.5)); ax.set_xlim(0, 160); ax.set_ylim(0, 95); ax.axis('off')
C = dict(pwr='#ffe3e3', sense='#e3f2ff', amp='#e6f7e6', mcu='#fff4cc', out='#f0e6ff', line='#333')

def box(x, y, w, h, title, lines, color, tsize=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=1.5', fc=color, ec=C['line'], lw=1.5))
    ax.text(x + w/2, y + h - 2, title, ha='center', va='top', fontsize=tsize, fontweight='bold')
    for i, t in enumerate(lines):
        ax.text(x + 1.5, y + h - 6.5 - i*3.4, t, ha='left', va='top', fontsize=8.6)

def arrow(x0, y0, x1, y1, label=None, color='#444', lw=2):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', color=color, lw=lw))
    if label: ax.text((x0+x1)/2, (y0+y1)/2 + 1.6, label, ha='center', fontsize=8.5, color=color)

ax.text(80, 92.5, 'Optical Heartbeat Detector — วงจรหลังต่อเสร็จ (ไฟ 5V จาก USB, Vref = 2.5V)', ha='center', fontsize=15, fontweight='bold')
ax.text(80, 89.3, 'draft 2026-10-17 · ค่าจากการคำนวณมือ ยังไม่ได้ทดสอบกับของจริง', ha='center', fontsize=9.5, color='#a00')

# row 1: transmit + sense
box(3, 62, 36, 24, '① ส่งแสง IR', ['+5V ─ R220 ─ IR LED(A→K)', '  ─ Q1 BC548 collector', 'Q1 emitter ─ GND', 'D9 ─ R1k ─ Q1 base', 'I(LED) ≈ 16 mA'], C['sense'])
box(48, 62, 36, 24, '② รับแสง', ['Phototransistor 940nm', ' ขายาว(collector) ─ +5V', ' ขาสั้น(emitter) ─ U1A pin2', 'นิ้วอยู่ระหว่าง ① กับ ②', 'มีผนังกันแสงตรงระหว่างกัน'], C['sense'])
box(93, 62, 36, 24, '③ U1A  transimpedance', ['LM358 #1 : pin8=+5V pin4=GND', 'pin2 (−) ← phototransistor', 'pin3 (+) ← Vref', 'Rf R4.7k ∥ Cf C10nF', '   คร่อม pin1─pin2', 'out = pin1'], C['amp'])

# row 2: amplifier chain, signal flows right -> left
box(93, 30, 36, 25, '④ HPF 0.16 Hz', ['pin1(U1A) ─ C10µF(+) ─ node X', 'X ─ R100k ─ Vref', 'X ─ U1B pin5 (+)', 'ตัด DC และแสงห้องที่นิ่ง'], C['amp'])
box(48, 30, 36, 25, '⑤ U1B  ขยาย', ['LM358 #1 (ตัวเดียวกับ U1A)', 'pin6 (−) ─ R2.4k ─ Vref', 'VR100k ∥ C10nF คร่อม pin7─pin6', 'gain 1…43 เท่า (หมุน VR)'], C['amp'])
box(3, 30, 36, 25, '⑥ LPF 3.4 Hz → A0', ['pin7(U1B) ─ R100k ─ node Y', 'Y ─ C470nF ─ GND', 'Y ─────────→ Arduino A0', 'สัญญาณกลาง ~2.5V'], C['amp'])

# row 3
box(3, 3, 36, 23, '⑦ Arduino Leonardo', ['A0  ← node Y', 'D9  → Q1 (IR)    D8 → Q2', 'D2 SDA / D3 SCL → OLED', '5V, GND → breadboard'], C['mcu'])
box(48, 3, 36, 23, 'Vref 2.5V', ['+5V ─ R10k ─ node V', 'node V ─ R10k ─ GND', 'node V ─ C10µF ─ GND', 'node V → pin3 U1A, R100k(HPF), R2.4k'], C['pwr'])
box(93, 3, 36, 23, '⑧ LED ชีพจร (Q2)', ['D8 ─ R1k ─ Q2 base (BC548)', '+5V ─ R470 ─ LED แดง', '  ─ Q2 collector', 'Q2 emitter ─ GND'], C['out'])
box(133, 3, 25, 23, '⑨ OLED', ['SSD1306 0x3C', 'GND─GND', 'VCC─5V', 'SDA─D2  SCL─D3'], C['out'])

arrow(39, 74, 48, 74, 'แสง IR ทะลุนิ้ว', '#c00')
arrow(84, 74, 93, 74, 'กระแสแสง')
arrow(111, 62, 111, 55.5, 'pin1 → ④')
arrow(93, 42, 84.5, 42)
arrow(48, 42, 39.5, 42)
arrow(21, 30, 21, 26.5, 'A0')
ax.text(80, 0.2, 'ทิศสัญญาณ: ① IR → นิ้ว → ② → ③ → ④ → ⑤ → ⑥ → A0  (แถวกลางไหลขวา→ซ้าย)', ha='center', fontsize=9)
fig.savefig(OUT, dpi=110, bbox_inches='tight')
print(OUT)
