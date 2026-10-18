import runpy, json
B = runpy.run_path('/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/breadboard_simple.py')
parts, wires, flying = B['parts'], B['wires'], B['flying']
NAMES = {0: 'LM358 (U1 บัฟเฟอร์)', 1: 'R10k โหลด PT', 2: 'Q1 BC548', 3: 'R1k ฐาน Q1', 4: 'R220 IR LED'}
KIND = {'ic': 'ic', 'res': 'res', 'npn': 'npn'}
BR = ['brown', 'black', 'orange', 'gold']
CODES = {0: dict(code='LM358P', no=1), 1: dict(code='น้ำตาล-ดำ-ส้ม-ทอง', bands=['brown', 'black', 'orange', 'gold'], no=16), 2: dict(code='BC548', no=2),
         3: dict(code='น้ำตาล-ดำ-แดง-ทอง', bands=['brown', 'black', 'red', 'gold'], no=13), 4: dict(code='แดง-แดง-น้ำตาล-ทอง', bands=['red', 'red', 'brown', 'gold'], no=11)}
out = {'parts': [], 'wires': [], 'ports': []}
for i, p in enumerate(parts):
    d = dict(id=f'p{i}', label=NAMES[i], kind=KIND[p['kind']], pins=[[c, r, n] for c, r, n in p['pins']], roles=None); d.update(CODES[i])
    if p['kind'] == 'npn': d['signs'], d['snote'] = ['C', 'B', 'E'], ['ซ้าย (หน้าแบนหันหาตัวเรา)', 'กลาง', 'ขวา']
    out['parts'].append(d)
for a, b, n in wires: out['wires'].append([list(a), list(b), n])
PORTS = {3: ('Arduino 5V', None, None), 4: ('Arduino GND', None, None), 2: ('Arduino A0', None, None), 5: ('Arduino D9', None, None),
         0: ('Phototransistor ขาสั้น (E)', ['E'], ['ขาสั้น (emitter) ต่อโหนดตัวรับ']), 1: ('Phototransistor ขายาว (C)', ['C'], ['ขายาว (collector) ต่อ 5V']),
         6: ('IR LED ขายาว (A)', ['+'], ['ขายาว (A แอโนด)']), 7: ('IR LED ขาสั้น (K)', ['−'], ['ขาสั้น (K แคโทด)'])}
PC = {0: ('Phototransistor 5mm 940nm (หัวดำ)', 4), 1: ('Phototransistor 5mm 940nm (หัวดำ)', 4), 6: ('IR LED 5mm 940nm (หัวใส)', 5), 7: ('IR LED 5mm 940nm (หัวใส)', 5)}
for i, (a, n, tag) in enumerate(flying):
    if i in PORTS:
        d = dict(id=f'f{i}', label=PORTS[i][0], hole=list(a), net=n)
        if PORTS[i][1]: d['signs'], d['snote'] = PORTS[i][1], PORTS[i][2]
        if i in PC: d['code'], d['no'] = PC[i]
        out['ports'].append(d)
json.dump(out, open('/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/bbsim_data_simple.json', 'w'), ensure_ascii=False)
print(len(out['parts']), len(out['wires']), len(out['ports']))
