# Optical Heartbeat Detector

Mini-project 1/2026 — วัดชีพจรด้วยแสงอินฟราเรด (IR LED + phototransistor → LM358 → Arduino A0) ใช้เฉพาะอุปกรณ์ในกล่องยืม

> สถานะ: ออกแบบ จำลอง (ngspice) และทำรูป/เว็บจำลองแล้ว **ยังไม่ได้ต่อและวัดกับของจริง**

- `08_firmware/` — โค้ด Arduino (Leonardo/UNO) และตารางต่อสาย `README_wiring.md`
- `07_pcb/kicad/` — สคีแมติก KiCad (ERC ผ่าน ไม่มี error) พร้อม netlist และ BOM
- `10_manual/` — รูปต่อ breadboard ทีละขั้น (`step1-7.png`), สคีแมติก, ผลจำลอง และสคริปต์ที่สร้างรูปทั้งหมด
- `02_design/model.py`, `04_print_stl/`, `06_cad_export/` — เคส (ฐาน + ฝา) สร้างจาก Fusion 360

เว็บจำลอง: https://tanachat007.github.io/optical-heartbeat/ (เครื่องจำลองชีพจร, ต่อวงจรบนเบรดบอร์ดเห็นกระแสไฟวิ่ง, วงจร 3 มิติ) ไฟล์ต้นทางอยู่ใน `docs/` และ `10_manual/`
