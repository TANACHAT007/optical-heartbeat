# Live view of the heartbeat signal (plot mode of the Arduino sketch) with extra band-pass filtering,
# motion detection and an autocorrelation BPM estimate. Close the window to stop.
import sys, time, collections, glob, serial
import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc'); plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
PORT = sys.argv[1] if len(sys.argv) > 1 else (glob.glob('/dev/cu.usbmodem*') + glob.glob('/dev/cu.usbserial*'))[0]
FS = 50.0                                   # samples per second (one per 20 ms)
ser = serial.Serial(PORT, 115200, timeout=0.05); time.sleep(1.5); ser.reset_input_buffer(); ser.write(b'p')
N = 500
raw = collections.deque([0.0] * N, N); bp = collections.deque([0.0] * N, N)
slow = 0.0; sm = collections.deque([0.0] * 5, 5)
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(11, 6.5), gridspec_kw={'height_ratios': [3, 1]}); fig.canvas.manager.set_window_title('Optical Heartbeat - live signal')
l_raw, = ax.plot(raw, color='#bbbbbb', lw=1, label='สัญญาณดิบ (หลังตัดค่านิ่ง)'); l_bp, = ax.plot(bp, color='#8b5cf6', lw=2.4, label='กรองเฉพาะย่านชีพจร 0.7–3 Hz')
ax.set_ylim(-5, 5); ax.grid(alpha=.3); ax.legend(loc='upper right', fontsize=9); ax.set_ylabel('ADC count'); ax.set_xticks([])
ttl = ax.set_title('วางนิ้วเบา ๆ นิ่ง ๆ รอ 8 วินาที')
l_ac, = ax2.plot([], [], color='#18b8a6', lw=2); ax2.set_xlabel('ระยะห่างของจังหวะ (วินาที) — ยอดที่ชัด = ชีพจรสม่ำเสมอ'); ax2.set_xlim(0.3, 1.6); ax2.set_ylim(-0.5, 1.05); ax2.grid(alpha=.3)
buf = b''; last_est = 0; status = ''
def estimate():
    x = np.array(bp)[-400:]
    if len(x) < 400 or np.abs(x).max() < 0.3: return None
    x = x - x.mean(); ac = np.correlate(x, x, 'full')[len(x) - 1:]; ac = ac / (ac[0] + 1e-9)
    lags = np.arange(len(ac)) / FS; m = (lags >= 0.4) & (lags <= 1.5)
    i = np.argmax(ac[m]); lag = lags[m][i]; return 60 / lag, float(ac[m][i]), lags[m], ac[m]
def upd():
    global buf, slow, last_est, status
    buf += ser.read(4096)
    while b'\n' in buf:
        ln, buf = buf.split(b'\n', 1)
        try: v = float(ln.decode().strip().split(',')[0])
        except Exception: continue
        raw.append(v); slow += (v - slow) * 0.02; sm.append(v - slow); bp.append(float(np.mean(sm)))
    l_raw.set_ydata(raw); l_bp.set_ydata(bp)
    a = np.abs(np.array(bp)); m = max(2.0, float(a.max()) * 1.2); ax.set_ylim(-m, m)
    if time.time() - last_est > 1.0:
        last_est = time.time(); e = estimate(); rms = float(np.std(np.array(bp)[-150:])); big = float(np.abs(np.array(bp)[-150:]).max()) > 6 * max(rms, 0.2)
        if e is None: status = 'สัญญาณเล็กมาก ยังไม่เห็นชีพจร'
        else:
            bpm, q, lg, ac = e; l_ac.set_data(lg, ac)
            if big: status = 'นิ้วขยับ/กดแรง — วางนิ้วให้นิ่ง (ผลประมาณ %.0f BPM ยังไม่เชื่อถือ)' % bpm
            elif q > 0.5: status = 'ชีพจร ≈ %.0f BPM   (ความสม่ำเสมอ %.0f%% — ดี)' % (bpm, q * 100)
            elif q > 0.3: status = 'ชีพจร ≈ %.0f BPM   (ความสม่ำเสมอ %.0f%% — พอใช้ วางให้นิ่งกว่านี้)' % (bpm, q * 100)
            else: status = 'ยังไม่ชัด (ความสม่ำเสมอ %.0f%%) ลองวางนิ้วให้นิ่ง' % (q * 100)
        ttl.set_text(status + '   · แกว่ง ±%.1f count' % float(a[-150:].max()))
plt.ion(); plt.show(block=False)
try:
    while plt.fignum_exists(fig.number):
        upd(); plt.pause(0.05)
finally:
    ser.write(b'p'); ser.close()
