# Simplified (single op-amp) front end: PT -> R10k load -> C10u -> LM358 non-inverting gain -> RC LPF -> A0
import numpy as np
import PySpice.Spice.NgSpice.Shared as S
S.NgSpiceShared.LIBRARY_PATH = '/Applications/KiCad/KiCad.app/Contents/PlugIns/sim/libngspice.dylib'
def net(i_dc, mod, vr_k, rate=1.2):
    return f"""* simple hb
V5 v5 0 5
Rd1 v5 vref 10k
Rd2 vref 0 10k
Cv vref 0 10u
Ipt 0 npt DC {i_dc} SIN({i_dc} {i_dc*mod} {rate} 0 0)
Rl npt 0 10k
Cc npt x 10u
Rb x vref 100k
Eg a1 0 x fb 1e5
Rp1 a1 b1 1k
Cp1 b1 0 15.9u
Bo1 oa0 0 V = max(0.05, min(3.5, V(b1)))
Ro1 oa0 oa 50
Rg fb vref 2.4k
Rv oa fb {vr_k*1000:.0f}
Cf oa fb 10n
Rlp oa y 100k
Cl y 0 470n
.ic v(vref)=2.5 v(x)=2.5 v(oa)=2.5 v(y)=2.5 v(fb)=2.5 v(npt)=0
.tran 5m 14 uic
.end
"""
def sim(i, m, vr):
    ng = S.NgSpiceShared.new_instance(); ng.load_circuit(net(i, m, vr)); ng.run()
    p = ng.plot(None, ng.last_plot); g = lambda k: np.array(p[k]._data if hasattr(p[k], '_data') else p[k])
    return g('time'), g('npt'), g('x'), g('oa'), g('y')
if __name__ == '__main__':
    for i, m, vr in [(30e-6, .01, 100), (100e-6, .01, 100), (100e-6, .01, 50), (200e-6, .01, 100), (400e-6, .01, 100), (100e-6, .003, 100)]:
        t, npt, x, oa, y = sim(i, m, vr); k = t > 9; pp = y[k].max() - y[k].min()
        print(f'Idc={i*1e6:4.0f}uA mod={m*100:3.1f}% VR={vr:3d}k | PT node DC={npt[k].mean():4.2f}V  A0 mean={y[k].mean():4.2f}V pp={pp*1000:6.1f}mV = {pp/5*1023:5.1f} counts')
