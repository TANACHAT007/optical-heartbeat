# Generates heartbeat.kicad_sch from a netlist-like part list using real KiCad library symbols (net labels on every pin).
import re, uuid, sys
sys.path.insert(0, '/Users/tanachat.s/fusion-projects/optical-heartbeat/07_pcb/kicad')
import kilib
from kilib import get_symbol, block, pins
OUT = '/Users/tanachat.s/fusion-projects/optical-heartbeat/07_pcb/kicad/heartbeat.kicad_sch'
U = lambda: str(uuid.uuid4())
ROOT = U()

def flat(lib, name):
    t = get_symbol(lib, name)
    m = re.search(r'\(extends "([^"]+)"\)', t)
    if not m: return t
    parent = flat(lib, m.group(1)); pn = m.group(1)
    parent = parent.replace('(symbol "%s"' % pn, '(symbol "%s"' % name, 1)
    parent = re.sub(r'\(symbol "%s_(\d+)_(\d+)"' % re.escape(pn), r'(symbol "%s_\1_\2"' % name, parent)
    return parent
def pins_flat(text, name): return pins(text, name)

# (ref, lib, symbol, value, x, y, {pin: net}, unit)
P = []
def part(ref, lib, sym, value, x, y, nets, unit=1): P.append((ref, lib, sym, value, round(x / 2.54) * 2.54, round(y / 2.54) * 2.54, nets, unit))
# row 1 (y=60): sensor chain
part('Q2', 'Device', 'Q_Photo_NPN', 'Phototransistor 940nm', 40, 60, {'1': '+5V', '2': 'NPT'})
part('R1', 'Device', 'R', '10k', 80, 60, {'1': 'NPT', '2': 'GND'})
part('C1', 'Device', 'C_Polarized', '10uF', 120, 60, {'1': 'X', '2': 'NPT'})
part('R2', 'Device', 'R', '100k', 160, 60, {'1': 'X', '2': 'Vref'})
part('U1', 'Amplifier_Operational', 'LM358', 'LM358', 210, 60, {'3': 'X', '2': 'FB', '1': 'OUT'}, 1)
part('R3', 'Device', 'R', '2.4k', 250, 60, {'1': 'FB', '2': 'Vref'})
part('RV1', 'Device', 'R_Potentiometer', '100k', 290, 60, {'1': 'OUT', '2': 'FB', '3': 'FB'})
part('C2', 'Device', 'C', '10nF', 330, 60, {'1': 'OUT', '2': 'FB'})
# row 2 (y=130): filter + unused amp + power
part('R4', 'Device', 'R', '100k', 40, 130, {'1': 'OUT', '2': 'A0'})
part('C3', 'Device', 'C', '470nF', 80, 130, {'1': 'A0', '2': 'GND'})
part('U1', 'Amplifier_Operational', 'LM358', 'LM358', 130, 130, {'5': 'Vref', '6': 'UN', '7': 'UN'}, 2)
part('U1', 'Amplifier_Operational', 'LM358', 'LM358', 180, 130, {'8': '+5V', '4': 'GND'}, 3)
part('C4', 'Device', 'C', '100nF', 220, 130, {'1': '+5V', '2': 'GND'})
part('C5', 'Device', 'C_Polarized', '100uF', 260, 130, {'1': '+5V', '2': 'GND'})
part('R5', 'Device', 'R', '10k', 300, 130, {'1': '+5V', '2': 'Vref'})
part('R6', 'Device', 'R', '10k', 340, 130, {'1': 'Vref', '2': 'GND'})
part('C6', 'Device', 'C_Polarized', '10uF', 380, 130, {'1': 'Vref', '2': 'GND'})
# row 3 (y=200): IR driver + connectors
part('R7', 'Device', 'R', '1k', 40, 200, {'1': 'D9', '2': 'Q1B'})
part('Q1', 'Transistor_BJT', 'BC548', 'BC548', 90, 200, {'1': 'Q1C', '2': 'Q1B', '3': 'GND'})
part('R8', 'Device', 'R', '220', 140, 200, {'1': '+5V', '2': 'IRA'})
part('D1', 'Device', 'LED', 'IR LED 940nm', 180, 200, {'1': 'Q1C', '2': 'IRA'})
part('J1', 'Connector_Generic', 'Conn_01x06', 'Arduino Leonardo (5V GND A0 D9 D2 D3)', 260, 200, {'1': '+5V', '2': 'GND', '3': 'A0', '4': 'D9', '5': 'SDA', '6': 'SCL'})
part('J2', 'Connector_Generic', 'Conn_01x04', 'OLED 0.96in I2C (GND VCC SCL SDA)', 330, 200, {'1': 'GND', '2': '+5V', '3': 'SCL', '4': 'SDA'})

libsyms = {}; pinmap = {}
for ref, lib, sym, value, x, y, nets, unit in P:
    key = f'{lib}:{sym}'
    if key not in libsyms:
        t = flat(lib, sym).replace('(symbol "%s"' % sym, '(symbol "%s"' % key, 1)
        libsyms[key] = t; pinmap[key] = pins(t, sym)
for lib, sym in (('power', '+5V'), ('power', 'GND'), ('power', 'PWR_FLAG')):
    key = f'{lib}:{sym}'; t = flat(lib, sym).replace('(symbol "%s"' % sym, '(symbol "%s"' % key, 1); libsyms[key] = t; pinmap[key] = pins(t, sym)

out = []; ind = lambda s: s
def eff(sz=1.27, just=''): return f'(effects (font (size {sz} {sz})){just})'
def prop(name, val, x, y, hide=False): return f'\t\t(property "{name}" "{val}" (at {x:g} {y:g} 0) {eff().replace(")", ")", 1) if not hide else "(effects (font (size 1.27 1.27)) (hide yes))"})'
body = []
def sym_inst(key, ref, value, x, y, unit, pinnums):
    pl = ''.join(f'\n\t\t(pin "{n}" (uuid "{U()}"))' for n in pinnums)
    body.append(f'''\t(symbol (lib_id "{key}") (at {x:g} {y:g} 0) (unit {unit}) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{U()}")
\t\t(property "Reference" "{ref}" (at {x+3:g} {y-6:g} 0) {eff()})
\t\t(property "Value" "{value}" (at {x+3:g} {y-3.5:g} 0) {eff()})
\t\t(property "Footprint" "" (at {x:g} {y:g} 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Datasheet" "" (at {x:g} {y:g} 0) (effects (font (size 1.27 1.27)) (hide yes))){pl}
\t\t(instances (project "heartbeat" (path "/{ROOT}" (reference "{ref}") (unit {unit}))))
\t)''')
def wire(x0, y0, x1, y1): body.append(f'\t(wire (pts (xy {x0:g} {y0:g}) (xy {x1:g} {y1:g})) (stroke (width 0) (type default)) (uuid "{U()}"))')
def label(net, x, y, ang):
    just = 'left bottom' if ang in (0, 90) else 'right bottom'
    body.append(f'\t(label "{net}" (at {x:g} {y:g} {ang}) (effects (font (size 1.27 1.27)) (justify {just})) (uuid "{U()}"))')
pwr_n = [0]
def power(net, x, y):
    key = 'power:+5V' if net == '+5V' else 'power:GND'; pwr_n[0] += 1
    sym_inst(key, f'#PWR0{pwr_n[0]:02d}', net, x, y, 1, ['1'])
flag_done = set(); fl = [0]
for ref, lib, sym, value, x, y, nets, unit in P:
    key = f'{lib}:{sym}'
    allp = [p for p in pinmap[key] if p[0] in (0, unit)]
    sym_inst(key, ref, value, x, y, unit, [p[1] for p in allp])
    for (u, num, nm, px, py, ang, ln, pt) in allp:
        net = nets.get(num)
        if net is None: print('UNCONNECTED pin', ref, num, nm); continue
        ax_, ay_ = x + px, y - py
        import math
        dx, dy = -math.cos(math.radians(ang)), math.sin(math.radians(ang)); L = 5.08
        ex, ey = ax_ + dx * L, ay_ + dy * L
        wire(ax_, ay_, ex, ey)
        if net in ('+5V', 'GND'):
            power(net, ex, ey)
            if net not in flag_done and ref == 'J1':
                fl[0] += 1; sym_inst('power:PWR_FLAG', f'#FLG0{fl[0]}', 'PWR_FLAG', ex, ey, 1, ['1']); flag_done.add(net)
        else:
            angle = {(1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270}[(round(dx), round(dy))]
            label(net, ex, ey, angle)
txt = '\t(text "Optical Heartbeat Detector - simple 1-op-amp front end (v2)\\nPT -> R10k -> C10u -> LM358 gain (VR) -> RC LPF -> A0\\nParts: from lab loan box only (LM358, BC548, BC548, phototransistor, IR LED, R/C/VR)" (at 20 20 0) (effects (font (size 2.5 2.5)) (justify left)) (uuid "%s"))' % U()
sch = f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "9.0")
\t(uuid "{ROOT}")
\t(paper "A3")
\t(title_block (title "Optical Heartbeat Detector") (date "2026-10-17") (rev "2") (comment 1 "Mini-project 1/2026 - Arduino + LM358 + BC548"))
\t(lib_symbols
{chr(10).join(libsyms.values())}
\t)
{chr(10).join(body)}
{txt}
\t(sheet_instances (path "/" (page "1")))
)
'''
open(OUT, 'w').write(sch); print('written', OUT, len(P), 'parts')
