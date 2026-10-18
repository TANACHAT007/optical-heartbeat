import runpy, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc')
plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
D = '/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
sim = runpy.run_path(D + 'sim_simple.py')['sim']
cases = [(30e-6, .01, 100, 'กระแสแสงนิ่ง 30 µA, ชีพจร 1%, VR 100k'), (100e-6, .01, 100, 'กระแสแสงนิ่ง 100 µA, ชีพจร 1%, VR 100k'), (100e-6, .01, 50, 'กระแสแสงนิ่ง 100 µA, ชีพจร 1%, VR 50k (gain ลดลง)')]
fig, axs = plt.subplots(len(cases), 3, figsize=(17, 9.5))
for r, (i, mod, vr, ttl) in enumerate(cases):
    t, npt, x, oa, y = sim(i, mod, vr)
    axs[r, 0].plot(t, npt, color='#c60'); axs[r, 0].set_ylabel('แรงดันที่ PT (V)')
    axs[r, 1].plot(t, x, color='#7a3fb0'); axs[r, 1].set_ylabel('หลังตัด DC (X) (V)'); axs[r, 1].set_ylim(1.5, 3.5)
    axs[r, 2].plot(t, y, color='#0a8a3a'); axs[r, 2].set_ylabel('A0 (V)'); axs[r, 2].set_ylim(0, 5); axs[r, 2].axhline(2.5, color='#aaa', lw=.8, ls='--')
    ppy = y[t > 9].max() - y[t > 9].min(); axs[r, 2].text(0.02, 0.9, f'pp = {ppy*1000:.0f} mV ≈ {ppy/5*1023:.0f} count', transform=axs[r, 2].transAxes, fontsize=10, color='#063')
    axs[r, 0].set_title(ttl, loc='left', fontsize=10, fontweight='bold')
    for a in axs[r]: a.grid(alpha=.3); a.set_xlabel('เวลา (s)')
fig.suptitle('Simulation (ngspice) วงจรแบบง่าย: ชีพจร 72 BPM → A0   [โมเดล op-amp แบบง่าย ไม่ใช่ LM358 จริง]', fontsize=13, fontweight='bold')
fig.tight_layout(); fig.savefig(D + 'simulation.png', dpi=110); print('ok')
