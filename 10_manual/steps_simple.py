# Step-by-step breadboard pictures (one image per step, big and simple). Data comes from breadboard.py.
import runpy, math, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Wedge, Ellipse
D = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
B = runpy.run_path(D + 'breadboard_simple.py')
parts, wires, flying, H, ROWY, RAILY = B['parts'], B['wires'], B['flying'], B['H'], B['ROWY'], B['RAILY']
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc')
plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
NUM = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮'
WCOL = {'5V': '#e02020', 'GND': '#222222', 'VREF': '#1ea03c', 'X': '#8a3fb0', 'UN': '#888888'}
BANDC = ['#111', '#7a4b1b', '#d11', '#f08000', '#e8d000', '#2a9a2a', '#2a5fd0', '#8a3fb0', '#888', '#eee']
RAILNAME = {'T5V': 'แถบ 5V (แดง)', 'TVREF': 'แถบ Vref (2.5V)', 'BGND': 'แถบ GND (ล่าง)'}
def hn(c, r): return f'{c}{r}' if r in ROWY else f'{RAILNAME[r]} คอลัมน์ {c}'
def holes(c, r): return f'คอลัมน์ {c} แถว {r}' if r in ROWY else f'{RAILNAME[r]} (คอลัมน์ {c})'
def val(label):
    s = label.split('\n')[0].split(' ')[0].replace('Ω', ''); m = 1
    if s.lower().endswith('k'): m, s = 1e3, s[:-1]
    try: return float(s) * m
    except: return None

STEPS = [
 dict(t='ไฟเลี้ยง: Arduino 5V และ GND เข้าแถบไฟ', P=[], W=[], F=[3, 4], cols=(-1, 15)),
 dict(t='วาง LM358 แล้วต่อไฟขา 8 และ 4 ผูกขาที่ไม่ใช้ (5, 6, 7)', P=[0], W=[0, 1, 2, 3], F=[], cols=(20, 31)),
 dict(t='วงจรส่งแสง IR: Q1 + R1k + R220 + IR LED', P=[2, 3, 4], W=[6], F=[5, 6, 7], cols=(36, 48)),
 dict(t='ตัวรับแสง: phototransistor + R10k โหลด', P=[1], W=[], F=[0, 1], cols=(8, 22)),
 dict(t='บัฟเฟอร์: NPT → ขา 3 และขา 1 → ขา 2', P=[], W=[4, 5], F=[], cols=(12, 31)),
 dict(t='ส่งเข้า Arduino A0 จากขาออก (ขา 1)', P=[], W=[], F=[2], cols=(20, 31)),
]

def draw(step, idx):
    c0, c1 = step['cols']; new_p, new_w, new_f = set(step['P']), set(step['W']), set(step['F'])
    done_p = set(range(0, 0)); 
    prev = STEPS[:idx]
    old_p = {i for s in prev for i in s['P']}; old_w = {i for s in prev for i in s['W']}; old_f = {i for s in prev for i in s['F']}
    fig = plt.figure(figsize=(16, 11)); axb = fig.add_axes([0.0, 0.03, 0.56, 0.88]); axt = fig.add_axes([0.58, 0.03, 0.41, 0.88]); axt.axis('off'); axb.axis('off')
    axt.set_xlim(0, 1); axt.set_ylim(0, 1)
    axb.set_xlim(c0 - 1.3, c1 + 1.3); axb.set_ylim(-4.8, 19.4); axb.set_aspect('equal')
    ax = axb
    ax.add_patch(FancyBboxPatch((c0 - 0.8, -1.9), c1 - c0 + 1.6, 18, boxstyle='round,pad=0.1,rounding_size=0.4', fc='#f6f4ee', ec='#bdb8a8', lw=2, zorder=1))
    ax.add_patch(Rectangle((c0 - .7, 6.15), c1 - c0 + 1.4, 0.7, fc='#e2ddcd', ec='none', zorder=2))
    for yy, c in ((15.75, '#d62c2c'), (13.75, '#bbb'), (-0.7, '#2c5fd6')): ax.plot([c0 - .6, c1 + .6], [yy, yy], color=c, lw=2, zorder=2)
    for col in range(max(1, c0), c1 + 1):
        for r in list(ROWY) + list(RAILY): ax.add_patch(Rectangle((col - .17, H(col, r)[1] - .17), .34, .34, fc='#6b6b6b', ec='none', zorder=3))
        ax.text(col, 12.55, str(col), ha='center', fontsize=9, color='#888', zorder=3)
    for r, y in ROWY.items(): ax.text(c0 - 0.45, y, r, ha='center', va='center', fontsize=10, color='#888', zorder=3)
    ax.text(c0 - .6, 15.2, '+5V', ha='right', va='center', fontsize=10, color='#d62c2c', fontweight='bold'); ax.text(c0 - .6, 14.2, '(ไม่ใช้)', ha='right', va='center', fontsize=8, color='#999'); ax.text(c0 - .6, -0.2, 'GND', ha='right', va='center', fontsize=10, color='#2c5fd6', fontweight='bold')
    lines = []; n = [0]
    def badge(x, y, k, col):
        ax.add_patch(Circle((x, y), 0.62, fc='#ffffff', ec=col, lw=3, zorder=40)); ax.text(x, y, NUM[k], ha='center', va='center', fontsize=17, fontweight='bold', color=col, zorder=41)
    def inrange(*cs): return all(c0 - 1 <= c <= c1 + 1 for c in cs)
    # parts
    for i, p in enumerate(parts):
        isnew = i in new_p
        if not (isnew or i in old_p): continue
        cs = [c for c, r, _ in p['pins']]
        if not inrange(*cs): continue
        al = 1.0 if isnew else 0.28
        P = [H(c, r) for c, r, _ in p['pins']]; k = p['kind']; z = 10 if isnew else 5
        cx0 = sum(x for x, y in P) / len(P); cy0 = sum(y for x, y in P) / len(P)
        if k == 'res':
            (x0, y0), (x1, y1) = P[:2]; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; ang = math.degrees(math.atan2(y1 - y0, x1 - x0)); d = math.hypot(x1 - x0, y1 - y0); bl = min(2.8, d * .8); u = ((x1 - x0) / d, (y1 - y0) / d)
            ax.plot([x0, cx - u[0] * bl / 2], [y0, cy - u[1] * bl / 2], color='#aaa', lw=3, alpha=al, zorder=z); ax.plot([x1, cx + u[0] * bl / 2], [y1, cy + u[1] * bl / 2], color='#aaa', lw=3, alpha=al, zorder=z)
            t = matplotlib.transforms.Affine2D().rotate_deg_around(cx, cy, ang) + ax.transData
            r_ = FancyBboxPatch((cx - bl / 2, cy - .5), bl, 1.0, boxstyle='round,pad=0,rounding_size=.4', fc='#e3c79a', ec='#9c7f4c', lw=1.5, alpha=al, zorder=z + 1); r_.set_transform(t); ax.add_patch(r_)
            v = val(p['label'])
            if v:
                e = int(math.floor(math.log10(v))) - 1; dd = int(round(v / 10 ** e)); bb = [dd // 10, dd % 10, e]
                for j, cc in enumerate([BANDC[bb[0]], BANDC[bb[1]], BANDC[bb[2]] if 0 <= bb[2] <= 9 else '#c9a227', '#c9a227']):
                    rr = Rectangle((cx - bl / 2 + .55 + j * .5 + (.4 if j == 3 else 0), cy - .48), .24, .96, fc=cc, ec='none', alpha=al, zorder=z + 2); rr.set_transform(t); ax.add_patch(rr)
            for q in P[:2]: ax.add_patch(Circle(q, .24, fc='#777', ec='none', alpha=al, zorder=z))
            lx, ly = cx, cy + 1.1
        elif k == 'cer':
            cx, cy = (P[0][0] + P[1][0]) / 2, max(P[0][1], P[1][1]) + 1.3
            for q, dx in zip(P, (-.4, .4)): ax.plot([q[0], cx + dx], [q[1], cy - .5], color='#aaa', lw=3, alpha=al, zorder=z)
            ax.add_patch(Ellipse((cx, cy), 1.7, 1.8, fc='#cc7a2e', ec='#7a4a18', lw=1.5, alpha=al, zorder=z + 1))
            if isnew: ax.text(cx, cy, p['label'].split('\n')[-1].strip('()'), ha='center', va='center', fontsize=8, color='#3a2200', zorder=z + 2)
            lx, ly = cx, cy + 1.2
        elif k == 'ele':
            (x0, y0), (x1, y1) = P[:2]; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; ang = math.degrees(math.atan2(y1 - y0, x1 - x0)); d = math.hypot(x1 - x0, y1 - y0); bl = min(3.0, d * .8); u = ((x1 - x0) / d, (y1 - y0) / d)
            ax.plot([x0, cx - u[0] * bl / 2], [y0, cy - u[1] * bl / 2], color='#aaa', lw=3, alpha=al, zorder=z); ax.plot([x1, cx + u[0] * bl / 2], [y1, cy + u[1] * bl / 2], color='#aaa', lw=3, alpha=al, zorder=z)
            t = matplotlib.transforms.Affine2D().rotate_deg_around(cx, cy, ang) + ax.transData
            b_ = FancyBboxPatch((cx - bl / 2, cy - .8), bl, 1.6, boxstyle='round,pad=0,rounding_size=.25', fc='#222c48', ec='#000', alpha=al, zorder=z + 1); b_.set_transform(t); ax.add_patch(b_)
            s_ = Rectangle((cx + bl / 2 - .75, cy - .8), .55, 1.6, fc='#eee', ec='none', alpha=al, zorder=z + 2); s_.set_transform(t); ax.add_patch(s_)
            if isnew: ax.text(x0 + (cx - x0) * .35, y0 + (cy - y0) * .35 + .7, '+', color='#ff3030', fontsize=22, fontweight='bold', zorder=z + 3, ha='center')
            lx, ly = cx, cy + 1.3
        elif k == 'ic':
            ax.add_patch(Rectangle((23.55, 5.45), 4.0, 2.4, fc='#1d1d1d', ec='#000', lw=1.6, alpha=al, zorder=z + 1)); ax.add_patch(Wedge((23.55, 6.65), .45, -90, 90, fc='#555', ec='none', alpha=al, zorder=z + 2))
            ax.text(25.6, 6.65, 'LM358', ha='center', va='center', color='#fff', fontsize=12, alpha=al, zorder=z + 3)
            for cc, nn in zip((24, 25, 26, 27), (1, 2, 3, 4)): ax.text(cc, 4.95, str(nn), ha='center', fontsize=10, color='#c60', fontweight='bold', alpha=al, zorder=z + 3)
            for cc, nn in zip((27, 26, 25, 24), (5, 6, 7, 8)): ax.text(cc, 8.25, str(nn), ha='center', fontsize=10, color='#c60', fontweight='bold', alpha=al, zorder=z + 3)
            ax.text(23.2, 6.65, 'รอยบาก ◖', ha='right', va='center', fontsize=8, color='#666', alpha=al, zorder=z + 3)
            lx, ly = 25.6, 9.3
        elif k == 'vr':
            ax.add_patch(Rectangle((28.3, 11.9), 5.4, 2.5, fc='#3a78c8', ec='#123', lw=1.8, alpha=al, zorder=z + 1)); ax.add_patch(Circle((31, 13.15), 1.0, fc='#d9c36a', ec='#7a6a1a', lw=1.5, alpha=al, zorder=z + 2))
            for (x, y) in P: ax.plot([x, x], [y, 11.9], color='#aaa', lw=3, alpha=al, zorder=z)
            for (x, y), nn in zip(P, '123'): ax.text(x, 12.3, nn, ha='center', va='center', fontsize=9, color='#fff', alpha=al, zorder=z + 3, fontweight='bold')
            lx, ly = 27.2, 13.2
        elif k == 'npn':
            for x, y in P: ax.plot([x, x], [y, y + 1.4], color='#aaa', lw=3, alpha=al, zorder=z)
            cx, cy = P[1][0], P[1][1] + 1.4
            ax.add_patch(Wedge((cx, cy), 1.4, 0, 180, fc='#1d1d1d', ec='#000', alpha=al, zorder=z + 1)); ax.add_patch(Rectangle((cx - 1.4, cy - .55), 2.8, .55, fc='#2b2b2b', ec='#000', alpha=al, zorder=z + 1))
            for (x, y), tt in zip(P, 'CBE'): ax.text(x, y - .85, tt, ha='center', fontsize=10, color='#06c', fontweight='bold', alpha=al, zorder=z + 3)
            lx, ly = cx, cy + 1.7
        if isnew:
            n[0] += 1; kk = n[0] - 1
            if k in ('res', 'cer', 'ele'):
                (ax0, ay0), (ax1, ay1) = P[:2]; dd_ = math.hypot(ax0 - ax1, ay0 - ay1) or 1
                bx_, by_ = ax0 + (ax0 - ax1) / dd_ * 1.1, ay0 + (ay0 - ay1) / dd_ * 1.1 + (0.0 if abs(ay0 - ay1) > .1 else 0)
                badge(bx_, by_, kk, '#d04a00')
            else: badge(lx, ly + .2, kk, '#d04a00')
            L = p['label'].replace('\n', ' ')
            if k == 'res': lines.append((kk, '#d04a00', f"{L}", f"เสียบที่ {hn(*p['pins'][0][:2])} และ {hn(*p['pins'][1][:2])}"))
            elif k == 'cer': lines.append((kk, '#d04a00', f"ตัวเก็บประจุ {L}", f"เสียบที่ {hn(*p['pins'][0][:2])} และ {hn(*p['pins'][1][:2])} (ไม่มีขั้ว)"))
            elif k == 'ele': lines.append((kk, '#d04a00', f"ตัวเก็บประจุ {L}", f"ขา + (ขายาว) ลง {hn(*p['pins'][0][:2])} · ขา − ลง {hn(*p['pins'][1][:2])}"))
            elif k == 'ic': lines.append((kk, '#d04a00', 'LM358', 'คร่อมร่องกลาง รอยบากซ้าย: ขา 1 ที่ 24f · ขา 8 ที่ 24e'))
            elif k == 'vr': lines.append((kk, '#d04a00', 'VR100k', 'ขา 1→29a · ขา 2 (กลาง)→31a · ขา 3→33a'))
            elif k == 'npn': lines.append((kk, '#d04a00', p['label'].split('\n')[0] + ' BC548', f"หน้าแบนหันหาตัวเรา ขาซ้าย→ขวา (C,B,E) = {hn(*p['pins'][0][:2])}, {hn(*p['pins'][1][:2])}, {hn(*p['pins'][2][:2])}"))
    # wires
    for i, (a, b, nn) in enumerate(wires):
        isnew = i in new_w
        if not (isnew or i in old_w) or not inrange(a[0], b[0]): continue
        col = WCOL.get(nn, '#2f6fe0'); al = 1.0 if isnew else 0.28
        (x0, y0), (x1, y1) = H(*a), H(*b)
        ax.plot([x0, x1], [y0, y1], color=col, lw=5.5, alpha=al, zorder=20 if isnew else 6, solid_capstyle='round')
        for x, y in ((x0, y0), (x1, y1)): ax.add_patch(Circle((x, y), .34, fc=col, ec='#000', lw=.8, alpha=al, zorder=21 if isnew else 7))
        if isnew:
            n[0] += 1; kk = n[0] - 1; dw_ = math.hypot(x0 - x1, y0 - y1) or 1
            badge(x0 + (x0 - x1) / dw_ * 1.1, y0 + (y0 - y1) / dw_ * 1.1, kk, col if col != '#222222' else '#222')
            cname = {'5V': 'แดง', 'GND': 'ดำ', 'VREF': 'เขียว', 'X': 'ม่วง', 'UN': 'เทา'}.get(nn, 'น้ำเงิน')
            lines.append((kk, col, f'สาย{cname}', f'{hn(*a)}  ↔  {hn(*b)}'))
    # flying leads / external
    for i, (a, nn, tag) in enumerate(flying):
        isnew = i in new_f
        if not isnew or not inrange(a[0]): continue
        x, y = H(*a); col = WCOL.get(nn, '#2f6fe0'); up = y > 6.5
        ty = 17.0 if (up or a[1] in ('T5V', 'TVREF')) else -2.7
        ax.plot([x, x], [y, ty], color=col, lw=4.5, ls=(0, (3, 2)), zorder=20); ax.add_patch(Circle((x, y), .34, fc=col, ec='#000', lw=.8, zorder=21))
        ax.text(x, ty + (.3 if ty > y else -.3), tag.replace('\n', ' '), ha='center', va='bottom' if ty > y else 'top', fontsize=10.5, color=col if col != '#222222' else '#222', fontweight='bold', zorder=30, bbox=dict(fc='white', ec=col, boxstyle='round', alpha=.95))
        n[0] += 1; kk = n[0] - 1; badge(x + 1.1, y, kk, col if col != '#222222' else '#222')
        lines.append((kk, col, tag.replace('\n', ' '), f'ต่อเข้า {hn(*a)} (สายยาว/จั๊มเปอร์)'))
    fig.suptitle(f'ขั้นที่ {idx + 1} / {len(STEPS)}:  {step["t"]}', fontsize=20, fontweight='bold', x=0.5, y=0.97)
    axt.text(0.0, 0.99, 'ทำตามลำดับตัวเลข', fontsize=15, fontweight='bold', va='top')
    ax.text((c0 + c1) / 2, -4.5, 'ของจางๆ = ต่อไว้แล้วจากขั้นก่อน · ของสีเข้ม + เลขวงกลม = ของที่ต้องต่อในขั้นนี้', ha='center', fontsize=10.5, color='#555')
    y = 0.93
    for kk, col, a_, b_ in lines:
        axt.add_patch(Circle((0.03, y - 0.012), 0.022, fc='#fff', ec=col, lw=2.5, transform=axt.transAxes, clip_on=False)); axt.text(0.03, y - 0.012, NUM[kk], ha='center', va='center', fontsize=13, fontweight='bold', color=col if col != '#222222' else '#222')
        axt.text(0.075, y, a_, fontsize=12.5, fontweight='bold', va='top'); axt.text(0.075, y - 0.032, b_, fontsize=10.5, va='top', color='#333', wrap=True)
        y -= 0.088 if len(b_) < 52 else 0.106
    out = D + f'simple_step{idx + 1}.png'
    fig.savefig(out, dpi=88); plt.close(fig); return out

for i, s in enumerate(STEPS): print(draw(s, i))
