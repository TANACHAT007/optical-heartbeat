# Live plot of the heartbeat signal from the Arduino (plot mode). Close the window to stop.
import sys, time, collections, serial
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('/System/Library/Fonts/Supplemental/Thonburi.ttc'); plt.rcParams['font.family'] = ['Thonburi', 'DejaVu Sans']
import glob
PORT = sys.argv[1] if len(sys.argv) > 1 else (glob.glob('/dev/cu.usbmodem*') + glob.glob('/dev/cu.usbserial*'))[0]
ser = serial.Serial(PORT, 115200, timeout=0.05); time.sleep(1.5); ser.reset_input_buffer(); ser.write(b'p')   # 'p' = plot mode
N = 600; sig = collections.deque([0] * N, N); thr = collections.deque([0] * N, N); nthr = collections.deque([0] * N, N)
fig, ax = plt.subplots(figsize=(11, 5)); fig.canvas.manager.set_window_title('Optical Heartbeat - live signal')
l1, = ax.plot(sig, color='#8b5cf6', lw=2, label='สัญญาณชีพจร (หลังกรอง)'); l2, = ax.plot(thr, '--', color='#ef4444', label='เกณฑ์ตรวจจับ'); ax.plot(nthr, '--', color='#ef4444', alpha=.3)
ax.set_ylim(-150, 150); ax.set_xlabel('เวลา (ตัวอย่างละ 10 ms, แสดง 6 วินาที)'); ax.set_ylabel('ADC count'); ax.grid(alpha=.3); ax.legend(loc='upper right')
ttl = ax.set_title('วางนิ้วเบา ๆ แล้วรอ 5-6 วินาที · ปิดหน้าต่างเพื่อหยุด')
buf = b''
def upd():
    global buf
    buf += ser.read(4096)
    while b'\n' in buf:
        ln, buf = buf.split(b'\n', 1)
        try:
            a, b, c = [float(x) for x in ln.decode().strip().split(',')]
            sig.append(a); thr.append(b); nthr.append(c)
        except Exception: pass
    l1.set_ydata(sig); l2.set_ydata(thr); ax.lines[2].set_ydata(nthr)
    m = max(4, max(abs(v) for v in sig) * 1.3); ax.set_ylim(-m, m)
    ttl.set_text('แกว่ง ±%d count · เกณฑ์ ±%d' % (max(abs(v) for v in sig), thr[-1]))
plt.ion(); plt.show(block=False)
try:
    while plt.fignum_exists(fig.number):
        upd(); plt.pause(0.05)
finally:
    ser.write(b'p'); ser.close()
