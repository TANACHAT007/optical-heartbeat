# เครื่องวัดชีพจรด้วยแสง Optical Heartbeat Detector — BOM (python make_bom.py) → bom.md + bom.csv next to this file
import os, csv, urllib.parse as u
HERE = os.path.dirname(os.path.abspath(__file__))
H = 'have'
rows = [  # group, item, spec, qty, unit THB (est.), status 'buy'|'buy?'|H, search keyword, note
]
def shopee(k): return 'https://shopee.co.th/search?keyword=' + u.quote(k) if k else ''
def lazada(k): return 'https://www.lazada.co.th/catalog/?q=' + u.quote(k) if k else ''
with open(os.path.join(HERE, 'bom.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['#', 'Group', 'Item', 'Spec', 'Qty', 'Unit THB (est.)', 'Total THB', 'Status', 'Shopee', 'Lazada', 'Note'])
    for i, (g, it, sp, q, up, st, k, n) in enumerate(rows, 1):
        w.writerow([i, g, it, sp, q, up, round(q * up), st, shopee(k), lazada(k), n])
total = sum(round(q * up) for g, it, sp, q, up, st, k, n in rows if st.startswith('buy'))
out = ['# เครื่องวัดชีพจรด้วยแสง Optical Heartbeat Detector — รายการอุปกรณ์ (BOM)', '', 'ราคาเป็นราคาประมาณ — ลิงก์เป็นหน้าค้นหา', '',
       '| # | กลุ่ม | รายการ | สเปก | จำนวน | ราคา/หน่วย | รวม | สถานะ | ลิงก์ |', '|---|---|---|---|---|---|---|---|---|']
for i, (g, it, sp, q, up, st, k, n) in enumerate(rows, 1):
    s = 'มีแล้ว' if st == H else ('ซื้อ (ถ้ายังไม่มี)' if st == 'buy?' else 'ซื้อ')
    lk = f'[Shopee]({shopee(k)}) · [Lazada]({lazada(k)})' if k else '—'
    out.append(f'| {i} | {g} | {it} | {sp}{" — " + n if n else ""} | {q} | {up:g} | {round(q * up):,} | {s} | {lk} |')
out += ['', f'**รวมต้องซื้อ ≈ {total:,} บาท**']
open(os.path.join(HERE, 'bom.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('items', len(rows), 'total', total)
