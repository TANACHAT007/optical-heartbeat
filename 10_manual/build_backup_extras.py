# embeds schematic/wiring pictures in backup.html (data URIs) and adds the two-version nav bar to every page
import base64, io, re, sys
from PIL import Image
D = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
def uri(name, w=1500, q=82):
    im = Image.open(D + name).convert('RGB')
    if im.width > w: im = im.resize((w, int(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
# ---- backup page images
t = open(D + 'backup.html').read()
if 'id="pics"' not in t:
    steps = ''.join(f'<figure style="margin:0"><img alt="ขั้นที่ {i}" style="width:100%;border:2px solid var(--line);border-radius:14px" src="{uri(f"simple_step{i}.png",1100,80)}"><figcaption class="foot">ขั้นที่ {i}</figcaption></figure>' for i in range(1, 7))
    block = f'''<section class="card" id="pics">
    <h2>ลายวงจร (สคีแมติก)</h2>
    <div class="two"><img alt="สคีแมติกส่วนรับสัญญาณ" style="width:100%;background:#fff;border-radius:12px;border:2px solid var(--line)" src="{uri('schematic_simple_sheet1.png',900,85)}"><img alt="สคีแมติกส่วนส่งแสง IR" style="width:100%;background:#fff;border-radius:12px;border:2px solid var(--line)" src="{uri('schematic_simple_sheet2.png',900,85)}"></div>
    <h2 style="margin-top:14px">ภาพต่อจริงบน breadboard (สไตล์ Fritzing)</h2>
    <img alt="ภาพต่อบน breadboard" style="width:100%;border:2px solid var(--line);border-radius:14px;background:#fff" src="{uri('fritzing_simple.png',1500,82)}">
    <h2 style="margin-top:14px">ต่อทีละขั้น (เหมือนวงจรหลัก ที่เหลือแค่ 6 ขั้น)</h2>
    <div class="two">{steps}</div>
    <p class="foot" style="margin-top:6px">ของจางๆ = ต่อแล้วจากขั้นก่อน · สีเข้มพร้อมเลข = ต้องต่อในขั้นนี้ · เว็บแบบโต้ตอบ (ไฟวิ่ง ต่อทีละขั้น มัลติมิเตอร์ 3 มิติ) ดูแท็บด้านบน</p>
  </section>
  '''
    t = t.replace('<section class="card">\n    <h2>อุปกรณ์ (ใช้น้อยกว่าวงจรหลักมาก)</h2>', block + '<section class="card">\n    <h2>อุปกรณ์ (ใช้น้อยกว่าวงจรหลักมาก)</h2>', 1)
    assert 'id="pics"' in t
    open(D + 'backup.html', 'w').write(t)
# ---- nav bar
URL = dict(sim='https://claude.ai/artifact/Uc3e7NhHANJSQ7egNfhjBK', mb='https://claude.ai/artifact/TzwCZ8pBQMchQR68SE9md6', m3='https://claude.ai/artifact/9R2wbiCAyP1nwR1Rpdz3z4',
           sg='https://claude.ai/artifact/7RnQXg54rU7CsXi8KS7Y3M', sb='https://claude.ai/artifact/GbEfg4bbwwCtjWDBhVeJKj', s3='https://claude.ai/artifact/FUoHQZJudDMxnMsMRAtQ3R')
CSS = '''.tabs{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;font-family:'Sarabun',system-ui,sans-serif;font-size:13.5px;margin:0 0 12px;padding:8px 12px;border:2px solid var(--line);border-radius:16px;background:var(--card)}
.tabs .grp{font-weight:700;color:var(--muted);margin-left:6px}.tabs .grp:first-child{margin-left:0}
.tabs a{color:var(--fg);text-decoration:none;padding:3px 11px;border-radius:99px;border:2px solid transparent}
.tabs a:hover{border-color:var(--pink)}.tabs a.on{background:var(--pink);color:#fff;font-weight:700}'''
def nav(active):
    a = lambda k, label: f'<a href="{URL[k]}"' + (' class="on" aria-current="page"' if k == active else '') + f'>{label}</a>'
    return ('<nav class="tabs" aria-label="เลือกแบบวงจร"><span class="grp">แบบหลัก</span>' + a('sim', 'จำลอง') + a('mb', 'ต่อวงจร') + a('m3', '3 มิติ') +
            '<span class="grp">แบบง่าย (สำรอง)</span>' + a('sg', 'คู่มือ+โปรแกรม') + a('sb', 'ต่อวงจร') + a('s3', '3 มิติ') + '</nav>')
PAGES = {'sim_web.html': 'sim', 'bbsim_web.html': 'mb', 'view3d.html': 'm3', 'backup.html': 'sg', 'bbsim_simple.html': 'sb', 'view3d_simple.html': 's3'}
for f, k in PAGES.items():
    h = open(D + f).read()
    h = re.sub(r'<nav class="tabs".*?</nav>', '', h, flags=re.S)
    if '.tabs{' not in h: h = h.replace('</style>', CSS + '\n</style>', 1)
    h = h.replace('<div class="wrap">', '<div class="wrap">' + nav(k), 1) if '<div class="wrap">' in h else h
    open(D + f, 'w').write(h)
    print(f, 'nav' , 'class="tabs"' in h, len(h) // 1024, 'KB')
