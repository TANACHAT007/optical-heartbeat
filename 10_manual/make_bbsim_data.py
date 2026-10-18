import runpy, json
B = runpy.run_path('/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/breadboard.py')
parts, wires, flying = B['parts'], B['wires'], B['flying']
NAMES = {0: 'LM358 (U1)', 1: 'R10k โหลด PT', 2: 'C 10µF ตัด DC', 3: 'R100k ไบอัส', 4: 'R2.4k', 5: 'VR 100k', 6: 'C 10nF', 7: 'R100k กรอง (LPF)', 8: 'C 470nF', 9: 'C 100µF', 10: 'C 100nF', 11: 'R10k (Vref ล่าง)', 12: 'R10k (Vref บน)', 13: 'C 10µF (Vref)', 14: 'Q1 BC548', 15: 'R1k ฐาน Q1', 16: 'R220 IR LED'}
ROLES = {'ele': ['ขา + (ขายาว)', 'ขา −'], 'npn': ['C (ซ้าย)', 'B (กลาง)', 'E (ขวา)'], 'vr': ['ขา 1', 'ขา 2 (กลาง)', 'ขา 3']}
KIND = {'ic': 'ic', 'res': 'res', 'cer': 'cap', 'ele': 'ele', 'vr': 'vr', 'npn': 'npn'}
out = {'parts': [], 'wires': [], 'ports': []}
for i, p in enumerate(parts):
    out['parts'].append(dict(id=f'p{i}', label=NAMES[i], kind=KIND[p['kind']], pins=[[c, r, n] for c, r, n in p['pins']], roles=ROLES.get(p['kind'])))
for a, b, n in wires: out['wires'].append([list(a), list(b), n])
PORTS = {3: ('Arduino 5V', ['5V']), 4: ('Arduino GND', ['GND']), 2: ('Arduino A0', ['Y']), 5: ('Arduino D9', ['D9']), 0: ('Phototransistor ขาสั้น (E)', ['NPT']), 1: ('Phototransistor ขายาว (C)', ['5V']), 6: ('IR LED ขายาว (A)', ['IRA']), 7: ('IR LED ขาสั้น (K)', ['Q1C'])}
for i, (a, n, tag) in enumerate(flying):
    if i in PORTS: out['ports'].append(dict(id=f'f{i}', label=PORTS[i][0], hole=list(a), net=n))
json.dump(out, open('/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/bbsim_data.json', 'w'), ensure_ascii=False)
print(len(out['parts']), len(out['wires']), len(out['ports']))
