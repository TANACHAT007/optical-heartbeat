# Fritzing-style breadboard picture (matplotlib). Netlist data comes from breadboard.py (parts / wires / flying).
import runpy, math, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon, Wedge, Ellipse
D = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
B = runpy.run_path(D + 'breadboard_irtest.py')
parts, wires, flying, H = B['parts'], B['wires'], B['flying'], B['H']
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc')
plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
OUT = D + 'fritzing_irtest.png'

fig, ax = plt.subplots(figsize=(24, 15)); ax.set_xlim(-4, 66); ax.set_ylim(-9, 46); ax.axis('off'); ax.set_aspect('equal')
WCOL = {'5V': '#e02020', 'GND': '#202020', 'VREF': '#1ea03c'}
def poly(pts, col, lw=4.2, z=20, round_=True):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=col, lw=lw, zorder=z, solid_capstyle='round', solid_joinstyle='round')
    for x, y in (pts[0], pts[-1]): ax.add_patch(Circle((x, y), 0.26, fc=col, ec='#000', lw=.6, zorder=z+1))

# ---- breadboard body
ax.add_patch(FancyBboxPatch((0, -1.9), 53, 18, boxstyle='round,pad=0.15,rounding_size=0.5', fc='#f6f4ee', ec='#bdb8a8', lw=2, zorder=1))
ax.add_patch(Rectangle((0.3, 6.15), 52.4, 0.7, fc='#e2ddcd', ec='none', zorder=2))
for yy, c in ((15.75, '#d62c2c'), (13.75, '#2c5fd6'), (-0.7, '#2c5fd6'), (-1.55, '#d62c2c')):
    ax.plot([0.7, 52.3], [yy, yy], color=c, lw=1.4, zorder=2)
for col in range(1, 53):
    for r in B['ROWY']: ax.add_patch(Rectangle((col-.17, B['ROWY'][r]-.17), .34, .34, fc='#6b6b6b', ec='none', zorder=3))
    for r in B['RAILY']: ax.add_patch(Rectangle((col-.17, B['RAILY'][r]-.17), .34, .34, fc='#6b6b6b', ec='none', zorder=3))
    if col % 5 == 0 or col == 1: ax.text(col, 12.55, str(col), ha='center', fontsize=7.5, color='#999', zorder=3)
for r, y in B['ROWY'].items(): ax.text(-0.45, y, r, ha='center', va='center', fontsize=8, color='#999', zorder=3)
for t, y, c in (('+ 5V', 15.2, '#d62c2c'), ('(ไม่ใช้)', 14.2, '#999'), ('− GND', -0.2, '#2c5fd6'), ('(ไม่ใช้)', -1.2, '#aaa')): ax.text(-1.0, y, t, ha='right', va='center', fontsize=8.5, color=c, fontweight='bold', zorder=3)

# ---- parts
BANDC = ['#111', '#7a4b1b', '#d11', '#f08000', '#e8d000', '#2a9a2a', '#2a5fd0', '#8a3fb0', '#888', '#eee']
def val(label):
    s = label.split('\n')[0].replace('Ω', ''); m = 1
    if s.lower().endswith('k'): m, s = 1e3, s[:-1]
    try: return float(s) * m
    except: return None
def bands(v):
    e = int(math.floor(math.log10(v))) - 1; d = int(round(v / 10**e)); 
    return [d // 10, d % 10, e]
def twoleg(pts, draw, lift=0.0):
    (x0, y0), (x1, y1) = pts; cx, cy = (x0+x1)/2, (y0+y1)/2 + lift
    return cx, cy, math.degrees(math.atan2(y1-y0, x1-x0)), math.hypot(x1-x0, y1-y0)
def rot(cx, cy, ang): return matplotlib.transforms.Affine2D().rotate_deg_around(cx, cy, ang) + ax.transData
def leg(a, b, col='#b9b9b9', lw=2.6): ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, zorder=6, solid_capstyle='round')

def txt(x, y, s, fs=7.5, col='#222', z=30):
    ax.text(x, y, s, ha='center', va='bottom', fontsize=fs, color=col, zorder=z, bbox=dict(fc='white', ec='none', alpha=.75, pad=.4))

for p in parts:
    k, pins, lab = p['kind'], p['pins'], p['label']
    P = [H(c, r) for c, r, n in pins]
    if k == 'res':
        cx, cy, ang, d = twoleg(P[:2], None); bl = 2.5
        u = ((P[1][0]-P[0][0])/d, (P[1][1]-P[0][1])/d)
        leg(P[0], (cx-u[0]*bl/2, cy-u[1]*bl/2)); leg(P[1], (cx+u[0]*bl/2, cy+u[1]*bl/2))
        r = FancyBboxPatch((cx-bl/2, cy-.42), bl, .84, boxstyle='round,pad=0,rounding_size=.35', fc='#e3c79a', ec='#9c7f4c', zorder=8); r.set_transform(rot(cx, cy, ang)); ax.add_patch(r)
        v = val(lab)
        if v:
            b = bands(v)
            for i, cc in enumerate([BANDC[b[0]], BANDC[b[1]], BANDC[b[2]] if 0 <= b[2] <= 9 else '#c9a227', '#c9a227']):
                bx = cx - bl/2 + 0.55 + i*0.45 + (0.35 if i == 3 else 0)
                rr = Rectangle((bx, cy-.4), .2, .8, fc=cc, ec='none', zorder=9); rr.set_transform(rot(cx, cy, ang)); ax.add_patch(rr)
        for q in P[:2]: ax.add_patch(Circle(q, .2, fc='#888', ec='none', zorder=7))
        txt(cx, cy + 0.75, lab.replace('\n', ' '))
    elif k == 'cer':
        cx, cy = (P[0][0]+P[1][0])/2, max(P[0][1], P[1][1]) + 1.15
        leg(P[0], (cx-.35, cy-.5)); leg(P[1], (cx+.35, cy-.5))
        ax.add_patch(Ellipse((cx, cy), 1.5, 1.6, fc='#cc7a2e', ec='#7a4a18', lw=1.4, zorder=8))
        ax.text(cx, cy, lab.split('\n')[-1].strip('()'), ha='center', va='center', fontsize=6.5, color='#3a2200', zorder=9)
        txt(cx, cy + 0.85, lab.split('\n')[0])
    elif k == 'ele':
        (x0, y0), (x1, y1) = P[:2]; cx, cy, ang, d = twoleg(P[:2], None); bl = 2.6
        u = ((x1-x0)/d, (y1-y0)/d)
        leg(P[0], (cx-u[0]*bl/2, cy-u[1]*bl/2)); leg(P[1], (cx+u[0]*bl/2, cy+u[1]*bl/2))
        body = FancyBboxPatch((cx-bl/2, cy-.7), bl, 1.4, boxstyle='round,pad=0,rounding_size=.2', fc='#222c48', ec='#000', zorder=8); body.set_transform(rot(cx, cy, ang)); ax.add_patch(body)
        st = Rectangle((cx+bl/2-.65, cy-.7), .5, 1.4, fc='#e8e8e8', ec='none', zorder=9); st.set_transform(rot(cx, cy, ang)); ax.add_patch(st)
        ax.text(x0 + (cx-x0)*0.3, y0 + (cy-y0)*0.3 + .45, '+', color='#ff4040', fontsize=14, fontweight='bold', zorder=12, ha='center')
        txt(cx, cy + 0.95, lab.replace('\n', ' '))
    elif k == 'ic':
        ax.add_patch(Rectangle((23.55, 5.55), 4.0, 2.2, fc='#1d1d1d', ec='#000', lw=1.5, zorder=8))
        ax.add_patch(Wedge((23.55, 6.65), .4, -90, 90, fc='#444', ec='none', zorder=9)); ax.text(25.6, 6.65, 'LM358', ha='center', va='center', color='#fff', fontsize=10, zorder=9)
        for c, n in zip((24, 25, 26, 27), (1, 2, 3, 4)): ax.add_patch(Rectangle((c-.16, 5.45), .32, .3, fc='#c8c8c8', ec='none', zorder=7)); ax.text(c, 5.0, str(n), ha='center', fontsize=7, color='#c60', zorder=9)
        for c, n in zip((27, 26, 25, 24), (5, 6, 7, 8)): ax.add_patch(Rectangle((c-.16, 7.5), .32, .3, fc='#c8c8c8', ec='none', zorder=7)); ax.text(c, 8.15, str(n), ha='center', fontsize=7, color='#c60', zorder=9)
    elif k == 'vr':
        ax.add_patch(Rectangle((28.3, 11.9), 5.4, 2.4, fc='#3a78c8', ec='#123', lw=1.6, zorder=8))
        ax.add_patch(Circle((31, 13.1), 1.0, fc='#d9c36a', ec='#7a6a1a', lw=1.5, zorder=9)); ax.plot([30.4, 31.6], [12.7, 13.5], color='#7a6a1a', lw=2, zorder=10)
        for (x, y) in P: leg((x, y), (x, 11.9))
        txt(31, 14.5, 'VR 100k (หมุนปรับ gain)')
    elif k == 'npn':
        (xc, yc), (xb, yb), (xe, ye) = P
        for x, y in P: leg((x, y), (x, y + 1.2))
        cx, cy = xb, yb + 1.2
        ax.add_patch(Wedge((cx, cy), 1.25, 0, 180, fc='#1d1d1d', ec='#000', zorder=8)); ax.add_patch(Rectangle((cx-1.25, cy-.5), 2.5, .5, fc='#2b2b2b', ec='#000', zorder=8))
        ax.text(cx, cy + .2, p['label'].split('\n')[1], ha='center', va='center', fontsize=6.5, color='#fff', zorder=9)
        for (x, y), t in zip(P, 'CBE'): ax.text(x, y - .75, t, ha='center', fontsize=7, color='#06c', zorder=9, fontweight='bold')
        txt(cx, cy + 1.3, p['label'].split('\n')[0] + ' (หน้าแบนหันหาตัวเรา)')

# ---- jumper wires inside the board
WC2 = {'XNET': '#8a3fb0', 'OUT_A': '#2f6fe0', 'OUT_B': '#2f6fe0', 'FB_A': '#2f6fe0', 'FB_B': '#e8c000', 'D9': '#f08000', 'D8': '#f08000'}
for a, b, n in wires:
    col = WCOL.get(n, WC2.get(n, '#777')); (x0, y0), (x1, y1) = H(*a), H(*b)
    poly([(x0, y0), (x1, y1)], col, lw=4.2, z=12)

# ---- Arduino Leonardo (USB left, digital header on top edge, power/analog on bottom edge)
ax.add_patch(FancyBboxPatch((6, 19.2), 27.5, 21, boxstyle='round,pad=0.1,rounding_size=0.8', fc='#0f6c8c', ec='#083f52', lw=2, zorder=2))
ax.add_patch(Rectangle((4.4, 27), 3.6, 5, fc='#bbb', ec='#555', zorder=3)); ax.text(6.2, 29.5, 'USB', ha='center', fontsize=7, color='#222', zorder=4)
ax.add_patch(Rectangle((14.5, 26), 5, 6, fc='#222', ec='#000', zorder=3)); ax.text(17, 29, 'ATmega32U4', ha='center', va='center', fontsize=7.5, color='#fff', zorder=4)
ax.text(24, 30, 'ARDUINO LEONARDO', ha='center', fontsize=13, color='#fff', fontweight='bold', zorder=4)
ax.add_patch(Rectangle((8, 20.4), 24.3, .9, fc='#222', ec='none', zorder=3)); ax.add_patch(Rectangle((8, 38.1), 24.3, .9, fc='#222', ec='none', zorder=3))
def pin(x, y, name, col='#111', up=True):
    ax.add_patch(Rectangle((x-.28, y-.28), .56, .56, fc='#e0c040', ec='#000', lw=.5, zorder=5))
    ax.text(x, y + (-1.0 if up is False else 1.0), name, ha='center', va='center', fontsize=6.8, color='#fff', rotation=0, zorder=5)
BOT = {'5V': 17, 'GND': 18, 'A0': 22}
for name, x in {'IOREF': 14, 'RST': 15, '3V3': 16, '5V': 17, 'GND': 18, 'GND ': 19, 'VIN': 20, 'A0': 22, 'A1': 23, 'A2': 24, 'A3': 25, 'A4': 26, 'A5': 27}.items(): pin(x, 20.85, name.strip(), up=True)
TOP = {'D9': 23, 'D8': 22, 'D3': 16, 'D2': 15}
for name, x in {'D13': 27, 'D12': 26, 'D11': 25, 'D10': 24, 'D9': 23, 'D8': 22, 'D7': 20, 'D6': 19, 'D5': 18, 'D4': 17, 'D3': 16, 'D2': 15, 'D1': 14, 'D0': 13}.items(): pin(x, 38.55, name, up=False)

OP={'GND':(0,0),'VCC':(0,0),'SCL':(0,0),'SDA':(0,0)}
# ---- sensor group (on the case lid): phototransistor + IR LED
ax.text(49, 26.2, 'ชุดเซนเซอร์ติดคู่กันที่ฝาเคส (ห่าง ~11 มม. หันขึ้นหานิ้ว)', fontsize=9, ha='center', color='#444', fontweight='bold')
def led(x, y, body, name):
    ax.add_patch(Wedge((x, y + 1.1), 1.05, 0, 180, fc=body, ec='#222', lw=1.4, zorder=8)); ax.add_patch(Rectangle((x-1.05, y), 2.1, 1.1, fc=body, ec='#222', lw=1.4, zorder=8)); ax.add_patch(Rectangle((x-1.25, y-.1), 2.5, .22, fc=body, ec='#222', zorder=8))
    ax.text(x, y + 2.9, name, ha='center', fontsize=8, color='#222', fontweight='bold')
SENS = {'IR': (51.3, 20.8), 'PT': (46.7, 20.8)}
led(*SENS['IR'], '#ececec', 'IR LED'); led(*SENS['PT'], '#2a2a2a', 'Phototransistor')
sp = {'IR_A': (SENS['IR'][0] - .45, SENS['IR'][1]), 'IR_K': (SENS['IR'][0] + .45, SENS['IR'][1]), 'PT_C': (SENS['PT'][0] - .45, SENS['PT'][1]), 'PT_E': (SENS['PT'][0] + .45, SENS['PT'][1])}
def hole(c, r): return H(c, r)
W = []
W.append(([(17, 20.85), (17, 18.2), (1, 18.2), hole(1, 'T5V')], '#e02020'))
W.append(([(18, 20.85), (18, 17.4), (-2.6, 17.4), (-2.6, -0.2), hole(1, 'BGND')], '#202020'))
W.append(([(22, 20.85), (22, 17.3), (16.6, 17.3), (16.6, 2.5), hole(14, 'i')], '#2f9fe0'))
W.append(([(23, 38.55), (23, 43.5), (57.5, 43.5), (57.5, -3.0), (44.6, -3.0), (44.6, 4.5), hole(43, 'g')], '#f08000'))
W.append(([sp['PT_E'], (sp['PT_E'][0], 18.4), (13.5, 18.4), (13.5, 4.5), hole(14, 'g')], '#2f6fe0'))
W.append(([sp['PT_C'], (sp['PT_C'][0], 19.2), (12, 19.2), hole(12, 'T5V')], '#e02020'))
W.append(([sp['IR_A'], (sp['IR_A'][0], 17.6), (44, 17.6), hole(44, 'b')], '#e02020'))
W.append(([sp['IR_K'], (sp['IR_K'][0], 17.1), (51.6, 17.1), (51.6, -2.4), (38, -2.4), hole(38, 'i')], '#555'))
for pts, col in W: poly(pts, col, lw=3.6, z=15)

ax.text(26.5, 45.4, 'Optical Heartbeat Detector — Breadboard view (สไตล์ Fritzing) — วงจรทดสอบ IR (ไม่ใช้ LM358)', ha='center', fontsize=17, fontweight='bold')
ax.text(26.5, -7.4, 'แถบไฟบน (แดง) = 5V · แถบล่าง = GND · แถบ Vref ไม่ใช้ในแบบนี้ · LED บอกชีพจรใช้ไฟบนบอร์ด Arduino (D13) · ภาพร่างจากการคำนวณ ยังไม่ได้ยืนยันกับของจริง', ha='center', fontsize=9.5, color='#444')
fig.savefig(OUT, dpi=90, bbox_inches='tight'); print(OUT)
