# Optical Heartbeat Detector

Mini-project 1/2026 — วัดชีพจรด้วยแสงอินฟราเรด (IR LED + phototransistor → LM358 → Arduino A0) ใช้เฉพาะอุปกรณ์ในกล่องยืม

> สถานะ (2026-10-18): ต่อวงจรจริงบน breadboard แล้ว ไฟ/Vref/ตัวขยาย/ตัวกรอง/วงจรส่งแสงทำงานตามที่วัดได้ **ยังไม่ได้ยืนยันสัญญาณชีพจรจริง** ดูบันทึกใน `08_firmware/BRINGUP.md`

- `08_firmware/` — โค้ด Arduino (Leonardo/UNO), ตารางต่อสาย `README_wiring.md`, บันทึกการทดสอบจริง `BRINGUP.md`, โปรแกรมวินิจฉัย `diag/` `d9test/` และกราฟสด `live_plot.py`
- `07_pcb/kicad/` — สคีแมติก KiCad (ERC ผ่าน ไม่มี error) พร้อม netlist และ BOM
- `10_manual/` — รูปต่อ breadboard ทีละขั้น (`step1-7.png`), สคีแมติก, ผลจำลอง และสคริปต์ที่สร้างรูปทั้งหมด
- `02_design/model.py`, `04_print_stl/`, `06_cad_export/` — เคส (ฐาน + ฝา) สร้างจาก Fusion 360

เว็บจำลอง: https://tanachat007.github.io/optical-heartbeat/ (เครื่องจำลองชีพจร, ต่อวงจรบนเบรดบอร์ดเห็นกระแสไฟวิ่ง, วงจร 3 มิติ) ไฟล์ต้นทางอยู่ใน `docs/` และ `10_manual/`

**วงจรสำรองแบบง่าย** (ตัวรับแสง → บัฟเฟอร์ LM358 → A0 ไม่มี Vref/ไบอัส/โวลุ่ม): โปรแกรม `08_firmware/heartbeat_backup/` และหน้า `docs/backup.html` (ตารางต่อ ค่าที่ต้องวัด ตัวจำลอง)

**รุ่นขยายสัญญาณของแบบง่าย** (ค่านิ่ง ×1 ส่วนชีพจรขยายด้วย VR ผ่าน C100µF ไม่ต้องมี Vref): ดูหัวข้อ 'อัปเกรด' ใน `docs/backup.html` สคีแมติก `10_manual/schematic_simple3.py` และภาพต่อบอร์ด `10_manual/fritzing_simple3.png`

**ทดสอบ IR ง่าย ๆ** (ไม่ใช้ LM358): โปรแกรม `08_firmware/irtest/` วงจร/ภาพต่อ/ตารางต่อในหัวข้อ 'ทดสอบ IR' ของ `docs/backup.html`
