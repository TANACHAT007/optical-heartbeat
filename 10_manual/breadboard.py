# Breadboard wiring picture + automatic netlist check. Run: python -I breadboard.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
import math, sys
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc')
plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
OUT = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/breadboard_wiring.png'

# ---------------- geometry ----------------
ROWY = dict(a=11.5, b=10.5, c=9.5, d=8.5, e=7.5, f=5.5, g=4.5, h=3.5, i=2.5, j=1.5)
RAILY = dict(T5V=15.2, TVREF=14.2, BGND=-0.2, BX=-1.2)
def H(col, row):
    return (col, ROWY[row]) if row in ROWY else (col, RAILY[row])
def key(col, row):
    if row in 'abcde' and row in ROWY: return ('c', col, 'U')
    if row in ROWY: return ('c', col, 'L')
    return ('r', row)

# ---------------- netlist ----------------
parts, wires, flying = [], [], []   # parts: dict(kind,label,pins=[(col,row,net)]) ; wires: (h1,h2,net)
def part(kind, label, pins, **kw): parts.append(dict(kind=kind, label=label, pins=pins, **kw))
def wire(a, b, net): wires.append((a, b, net))
def fly(a, net, tag): flying.append((a, net, tag))

# SIMPLE design: one op-amp stage. PT -> R10k load -> C10u -> U1 (non-inverting gain) -> RC LPF -> A0
# U1 LM358 (notch left): pins 1-4 on row f, 8-5 on row e. cols 24-27. Second op-amp (pins 5,6,7) is unused: pin6-7 tied, pin5 -> Vref
part('ic', 'LM358\n(U1)', [(24,'f','OUT'),(25,'f','FB'),(26,'f','X'),(27,'f','GND'),(27,'e','VREF'),(26,'e','UN'),(25,'e','UN'),(24,'e','5V')])
wire((24,'a'),(24,'T5V'),'5V'); wire((27,'g'),(27,'BGND'),'GND')
wire((26,'d'),(25,'d'),'UN'); wire((27,'d'),(27,'TVREF'),'VREF')
# phototransistor load + coupling + bias
fly((14,'g'),'NPT','Phototransistor\nขาสั้น (emitter)'); fly((12,'T5V'),'5V','Phototransistor\nขายาว (collector)')
part('res','R10k\n(โหลด PT)',[(14,'j','NPT'),(15,'BGND','GND')])
part('ele','10µF\n(ตัด DC)',[(20,'h','X'),(14,'h','NPT')])   # + on X (2.5 V side), - on NPT (~1 V)
wire((20,'g'),(26,'g'),'X')
part('res','R100k\n(ไบอัส)',[(20,'i','X'),(17,'i','VREF')])
wire((17,'TVREF'),(17,'j'),'VREF')
# gain network
part('res','R2.4k',[(25,'i','FB'),(22,'i','VREF')])
wire((22,'TVREF'),(22,'j'),'VREF')
part('vr','VR100k',[(29,'a','OUT'),(31,'a','FB'),(33,'a','FB')])
wire((24,'h'),(29,'b'),'OUT'); wire((25,'h'),(31,'b'),'FB'); wire((31,'c'),(33,'c'),'FB')
part('cer','10nF\n(103)',[(29,'e','OUT'),(31,'e','FB')])
# LPF -> A0
part('res','R100k\n(LPF)',[(24,'j','OUT'),(28,'j','Y')])
part('cer','470nF\n(474)',[(28,'i','Y'),(29,'BGND','GND')])
fly((28,'g'),'Y','→ Arduino A0')
# power + Vref
wire((3,'e'),(3,'T5V'),'5V'); wire((6,'e'),(6,'BGND'),'GND')
part('ele','100µF',[(3,'a','5V'),(6,'a','GND')])
part('cer','100nF\n(104)',[(3,'c','5V'),(6,'c','GND')])
part('res','R10k',[(6,'b','GND'),(9,'TVREF','VREF')])
part('res','R10k',[(10,'T5V','5V'),(13,'TVREF','VREF')])
part('ele','10µF\n(Vref)',[(11,'TVREF','VREF'),(6,'d','GND')])
fly((1,'T5V'),'5V','← Arduino 5V'); fly((1,'BGND'),'GND','← Arduino GND')
# Q1 + IR LED
part('npn','Q1\nBC548',[(38,'h','Q1C'),(39,'h','Q1B'),(40,'h','GND')])
wire((40,'j'),(40,'BGND'),'GND')
part('res','R1k',[(39,'i','Q1B'),(43,'i','D9')])
fly((43,'g'),'D9','← Arduino D9')
part('res','R220',[(41,'T5V','5V'),(44,'a','IRA')])
fly((44,'b'),'IRA','IR LED ขายาว (A)'); fly((38,'i'),'Q1C','IR LED ขาสั้น (K)')
# OLED (optional)
fly((50,'T5V'),'5V','OLED VCC'); fly((50,'BGND'),'GND','OLED GND')

# ---------------- verify ----------------
par = {}
def find(x):
    par.setdefault(x, x)
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
def union(a, b): par[find(a)] = find(b)
for a, b, _ in wires: union(key(*a), key(*b))
pins = [(p[0], p[1], p[2]) for pt in parts for p in pt['pins']] + [(a[0], a[1], n) for a, n, _ in flying]
for a, b, n in wires: pins += [(a[0], a[1], n), (b[0], b[1], n)]
net2root, root2net, errs, seen = {}, {}, [], {}
for c, r, n in pins:
    k = key(c, r); root = find(k)
    if n in net2root and net2root[n] != root: errs.append(f'net {n} split: {(c, r)}')
    net2root.setdefault(n, root)
    if root in root2net and root2net[root] != n: errs.append(f'short {n}<->{root2net[root]} at {(c, r)}')
    root2net.setdefault(root, n)
for pt in parts:
    for c, r, n in pt['pins']:
        if (c, r) in seen and seen[(c, r)] != pt['label']: errs.append(f'hole {(c, r)} used twice')
        seen[(c, r)] = pt['label']
print('NETLIST CHECK:', 'OK' if not errs else errs)
if errs: sys.exit(1)

# ---------------- draw ----------------
NETCOL = dict(GND='#222', **{'5V': '#d11'}, VREF='#0a8a3a')
fig, ax = plt.subplots(figsize=(22, 9.6)); ax.set_xlim(-1.5, 56.5); ax.set_ylim(-5.5, 20.5); ax.axis('off'); ax.set_aspect('equal')
ax.add_patch(FancyBboxPatch((0, -1.8), 53, 17.8, boxstyle='round,pad=0.2,rounding_size=0.6', fc='#f4f1e8', ec='#999', lw=1.5))
ax.add_patch(Rectangle((0.2, 6.2), 52.6, 0.6, fc='#ddd8c8', ec='none'))
for col in range(1, 53):
    for r in ROWY: ax.add_patch(Circle(H(col, r), 0.17, fc='#555', ec='none'))
    for r in RAILY: ax.add_patch(Circle(H(col, r), 0.17, fc='#555', ec='none'))
    if col % 5 == 0: ax.text(col, 12.6, str(col), ha='center', fontsize=7, color='#666')
for r, y in ROWY.items(): ax.text(-0.4, y, r, ha='center', va='center', fontsize=8, color='#666')
ax.plot([0.5, 52.5], [15.7, 15.7], color='#d11', lw=2); ax.text(-1.4, 15.2, '5V', color='#d11', fontsize=9, fontweight='bold', va='center')
ax.plot([0.5, 52.5], [13.7, 13.7], color='#0a8a3a', lw=2); ax.text(-1.4, 14.2, 'Vref', color='#0a8a3a', fontsize=9, fontweight='bold', va='center')
ax.plot([0.5, 52.5], [-0.7, -0.7], color='#222', lw=2); ax.text(-1.4, -0.2, 'GND', color='#222', fontsize=9, fontweight='bold', va='center')
ax.text(-1.4, -1.2, '(ไม่ใช้)', color='#888', fontsize=6, va='center')

def twoleg(p, body_len, draw_body, color_leg='#999'):
    (x0, y0), (x1, y1) = H(*p['pins'][0][:2]), H(*p['pins'][1][:2])
    cx, cy = (x0+x1)/2, (y0+y1)/2; ang = math.degrees(math.atan2(y1-y0, x1-x0)); d = math.hypot(x1-x0, y1-y0)
    u = ((x1-x0)/d, (y1-y0)/d); bl = min(body_len, d*0.7)
    a, b = (cx-u[0]*bl/2, cy-u[1]*bl/2), (cx+u[0]*bl/2, cy+u[1]*bl/2)
    ax.plot([x0, a[0]], [y0, a[1]], color=color_leg, lw=2, zorder=3); ax.plot([x1, b[0]], [y1, b[1]], color=color_leg, lw=2, zorder=3)
    draw_body(cx, cy, ang, bl)
    return cx, cy

def rect(cx, cy, ang, w, h, fc, z=5):
    t = matplotlib.transforms.Affine2D().rotate_deg_around(cx, cy, ang) + ax.transData
    r = Rectangle((cx-w/2, cy-h/2), w, h, fc=fc, ec='#333', lw=1.2, zorder=z); r.set_transform(t); ax.add_patch(r)
def lab(cx, cy, s, dy=0.9, fs=7.5, color='#111'):
    ax.text(cx, cy+dy, s, ha='center', va='bottom', fontsize=fs, color=color, zorder=9,
            bbox=dict(fc='white', ec='none', alpha=.8, pad=0.5))

for p in parts:
    k = p['kind']; pins = p['pins']
    if k == 'res':
        cx, cy = twoleg(p, 2.2, lambda cx, cy, ang, bl: rect(cx, cy, ang, bl, 0.75, '#e3c79a'))
        lab(cx, cy, p['label'])
    elif k == 'cer':
        cx, cy = twoleg(p, 1.0, lambda cx, cy, ang, bl: ax.add_patch(Circle((cx, cy), 0.55, fc='#d9893a', ec='#333', zorder=5)))
        lab(cx, cy, p['label'], 0.7)
    elif k == 'ele':
        def body(cx, cy, ang, bl):
            rect(cx, cy, ang, bl, 1.1, '#2a3550')
        cx, cy = twoleg(p, 1.9, body)
        (x0, y0) = H(*pins[0][:2]); ax.text(x0 + (cx-x0)*0.25, y0 + (cy-y0)*0.25 + 0.5, '+', fontsize=13, color='#c00', fontweight='bold', zorder=9, ha='center')
        lab(cx, cy, p['label'] + '\n(ขา + ตามรูป)', 0.9, 7)
    elif k == 'vr':
        xs = [H(*q[:2]) for q in pins]
        ax.add_patch(Rectangle((xs[0][0]-0.6, xs[0][1]+0.3), 5.2, 1.9, fc='#2e75b6', ec='#123', zorder=5))
        ax.add_patch(Circle((xs[1][0], xs[1][1]+1.25), 0.6, fc='#cfd8e3', ec='#123', zorder=6))
        for x, y in xs: ax.plot([x, x], [y, y+0.4], color='#999', lw=2, zorder=4)
        ax.text(xs[1][0], xs[1][1]+1.25, 'VR100k (ขา 1-2-3 → คอลัมน์ 15-17-19)', ha='center', va='center', fontsize=7, color='#fff', zorder=9)
    elif k == 'npn':
        xs = [H(*q[:2]) for q in pins]; cx = xs[1][0]; cy = xs[1][1] + 1.7
        ax.add_patch(Circle((cx, cy), 1.15, fc='#222', ec='#000', zorder=5))
        ax.add_patch(Rectangle((cx-1.15, cy-1.15), 2.3, 0.5, fc='#222', ec='none', zorder=5))
        ax.add_patch(Polygon([[cx-1.15, cy-0.35], [cx+1.15, cy-0.35], [cx+1.15, cy-1.15], [cx-1.15, cy-1.15]], fc='#444', ec='none', zorder=5)) if False else None
        for (x, y), t in zip(xs, 'CBE'):
            ax.plot([x, x], [y, cy-0.9], color='#999', lw=2, zorder=4); ax.text(x, y+0.35, t, fontsize=8, ha='center', color='#fff', zorder=9, fontweight='bold') if False else None
        for (x, y), t in zip(xs, 'CBE'): ax.text(x, y-0.9, t, fontsize=8, ha='center', color='#00f', fontweight='bold', zorder=9)
        ax.text(cx, cy, p['label'], ha='center', va='center', fontsize=7, color='#fff', zorder=9)
        ax.text(cx, cy+1.4, 'หน้าแบนหันหาตัวเรา', ha='center', fontsize=6.5, color='#555', zorder=9)
    elif k == 'ic':
        x0, x1 = 19.5, 23.5; ax.add_patch(Rectangle((x0, 5.8), x1-x0+0.0, 2.0, fc='#222', ec='#000', zorder=5))
        ax.add_patch(Circle((x0+0.1, 6.8), 0.35, fc='#666', ec='none', zorder=6))
        ax.text(21.5, 6.8, 'LM358  (U1)', ha='center', va='center', fontsize=8, color='#fff', zorder=9)
        for c, r, n in [(20,'f',1),(21,'f',2),(22,'f',3),(23,'f',4)]: ax.text(c, 5.0, str(n), fontsize=7, ha='center', color='#fa0', zorder=9)
        for c, r, n in [(23,'e',5),(22,'e',6),(21,'e',7),(20,'e',8)]: ax.text(c, 8.2, str(n), fontsize=7, ha='center', color='#fa0', zorder=9)
        ax.text(19.0, 6.8, 'รอยบาก←', fontsize=6.5, ha='right', va='center', color='#555')

# wires
WC = {'D9': '#e08000', 'D8': '#e08000', 'XNET': '#7a3fb0', 'OUT_A': '#1f6fd6', 'OUT_B': '#1f6fd6', 'FB_B': '#1f6fd6', 'FB_A': '#1f6fd6'}
for a, b, n in wires:
    (x0, y0), (x1, y1) = H(*a), H(*b)
    col = NETCOL.get(n, WC.get(n, '#888'))
    mx, my = (x0+x1)/2, (y0+y1)/2 + (0.0 if abs(x1-x0) < 0.1 else 0)
    ax.plot([x0, x1], [y0, y1], color=col, lw=3.0, zorder=4, solid_capstyle='round')
    for x, y in ((x0, y0), (x1, y1)): ax.add_patch(Circle((x, y), 0.28, fc=col, ec='#000', lw=.6, zorder=6))
# flying leads / external tags
for a, n, tag in flying:
    x, y = H(*a)
    up = y > 6.5 or a[1] in ('T5V', 'TVREF')
    ty = y + (4.2 if y > 6.5 else -3.4) + (0.0)
    ty = 18.6 if a[1] in ('T5V',) else (-3.6 if a[1] in ('BGND',) else (y + 4.0 if y > 6.5 else y - 3.3))
    if a[1] == 'T5V' or y > 6.5: ty = 18.3 if (a[0] % 2 == 0) else 17.0
    col = NETCOL.get(n, WC.get(n, '#888'))
    dx = 0.0
    ax.plot([x, x + dx], [y, ty], color=col, lw=2.2, ls=(0, (4, 2)), zorder=4)
    ax.add_patch(Circle((x, y), 0.28, fc=col, ec='#000', lw=.6, zorder=6))
    ax.text(x + dx, ty + (0.3 if ty > y else -0.3), tag, ha='center', va='bottom' if ty > y else 'top', fontsize=7.2, color=col, zorder=9, fontweight='bold')

ax.text(26.5, 19.9, 'Optical Heartbeat Detector — วิธีต่อบน Breadboard (ไฟจาก Arduino 5V เท่านั้น)', ha='center', fontsize=15, fontweight='bold')
ax.text(26.5, -4.7, 'เส้นประ = สายยาวไปอุปกรณ์นอกบอร์ด (เซนเซอร์/LED อยู่ที่ฝาเคส) · แถบไฟบนสุด = 5V, แถบไฟที่สอง = Vref 2.5V (ไม่ใช่ GND) · แถบล่าง = GND · ถ้า breadboard แถบไฟขาดกลางบอร์ด ให้ต่อสายคร่อม',
        ha='center', fontsize=8.8, color='#444')
fig.savefig(OUT, dpi=100, bbox_inches='tight'); print(OUT)
