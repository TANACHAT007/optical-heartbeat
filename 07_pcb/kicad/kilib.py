# tiny helpers to read KiCad symbol libraries (s-expression text slicing)
import re
SYM = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/'
def block(text, start):
    d = 0; i = start
    while True:
        c = text[i]
        if c == '(': d += 1
        elif c == ')':
            d -= 1
            if d == 0: return text[start:i+1]
        elif c == '"':
            i += 1
            while text[i] != '"':
                if text[i] == '\\': i += 1
                i += 1
        i += 1
def get_symbol(lib, name):
    t = open(SYM + lib + '.kicad_sym').read()
    m = re.search(r'\n\t\(symbol "%s"\n' % re.escape(name), t)
    assert m, (lib, name)
    return block(t, m.start() + 2)
def pins(sym_text, name):
    out = []   # (unit, number, pname, x, y, angle, length, ptype)
    for m in re.finditer(r'\(symbol "%s_(\d+)_(\d+)"' % re.escape(name.split(':')[-1]), sym_text):
        unit = int(m.group(1)); b = block(sym_text, m.start())
        for pm in re.finditer(r'\(pin (\w+) (\w+)\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)\s*\(length ([-\d.]+)\)', b):
            pb = block(b, pm.start())
            num = re.search(r'\(number "([^"]*)"', pb).group(1); nm = re.search(r'\(name "([^"]*)"', pb).group(1)
            out.append((unit, num, nm, float(pm.group(3)), float(pm.group(4)), float(pm.group(5)), float(pm.group(6)), pm.group(1)))
    return out
if __name__ == '__main__':
    for lib, n in [('Device', 'R'), ('Device', 'C'), ('Device', 'C_Polarized'), ('Device', 'LED'), ('Device', 'Q_Photo_NPN'), ('Device', 'R_Potentiometer'),
                   ('Transistor_BJT', 'BC548'), ('Amplifier_Operational', 'LM358'), ('Connector_Generic', 'Conn_01x04'), ('power', '+5V'), ('power', 'GND'), ('power', 'PWR_FLAG')]:
        s = get_symbol(lib, n)
        print(lib, n, 'extends' in s[:600], [(p[0], p[1], p[2], p[3], p[4], p[5], p[7]) for p in pins(s, n)])
