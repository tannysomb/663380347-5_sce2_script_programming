# Week 11 — LabX ADV: Project Planning & Design — Building an Enhanced Task Manager

**Agentic Document Automator** — ระบบจัดการเอกสารอัตโนมัติที่ขับเคลื่อนด้วยไฟล์ configuration
สามารถสร้างรายงาน Word จากเทมเพลต ใส่ลายน้ำลง PDF รวมไฟล์ PDF และดึงข้อความออกจากเอกสาร
โดยกำหนดงานทั้งหมดไว้ใน `configs/document_automation_config.json`

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **Config-Driven Document Pipeline** — นิยามงานทั้งหมดใน JSON เปลี่ยนงานได้โดยไม่ต้องแก้โค้ด
* **Template-Based Generation** — แทนที่ placeholder (`{{REPORT_TITLE}}`, `{{TABLE_PLACEHOLDER}}`) ในเทมเพลต Word ด้วยข้อมูลจริง
* **PDF Watermarking** — สร้างชั้นลายน้ำด้วย `reportlab` แล้วซ้อนทับหน้า PDF เดิมด้วย `PyPDF2`
* **PDF Merging & Text Extraction** — รวมไฟล์และดึงข้อความจากทั้ง PDF และ Word
* **Audit Logging** — บันทึกทุกขั้นตอนลงไฟล์ JSON ใน `documents/reports/`

## โครงสร้างโปรเจกต์

```text
week11_advanced/
├── src/
│   ├── __init__.py
│   ├── document_agent.py     # ตัวควบคุมหลัก อ่าน config แล้วสั่งงานทีละ task
│   ├── config_parser.py      # โหลดและตรวจสอบ config
│   ├── pdf_tasks.py          # รวม PDF, ใส่ลายน้ำ, ดึงข้อความ
│   ├── word_tasks.py         # สร้างรายงานจากเทมเพลต, ดึงข้อความ
│   └── utils.py              # logging และ audit log
├── configs/
│   └── document_automation_config.json
├── templates/
│   └── report_template.docx  # เทมเพลตที่มี placeholder
├── documents/
│   ├── source_document.pdf       # PDF ตั้งต้น
│   ├── dummy_doc1.pdf
│   ├── dummy_doc2.pdf
│   ├── generated_report.docx     # ผลลัพธ์ 1
│   ├── watermarked_document.pdf  # ผลลัพธ์ 2
│   ├── merged_docs.pdf           # ผลลัพธ์ 3
│   ├── extracted_word_text.txt
│   ├── extracted_pdf_text.txt
│   └── reports/audit_report_*.json
├── screenshots/              # ภาพผลลัพธ์ตามที่โจทย์กำหนดให้แนบ
├── main.py
└── README.md
```

## การติดตั้งและวิธีรัน

```bash
pip install PyPDF2 python-docx reportlab
python main.py
```

Agent ทำงาน 5 tasks ตามลำดับที่กำหนดใน config:

| # | Task | ผลลัพธ์ |
| --- | --- | --- |
| 1 | `generate_word_report` | สร้าง `generated_report.docx` จากเทมเพลต พร้อมตารางสรุป 4 แถว |
| 2 | `apply_pdf_watermark` | ใส่ลายน้ำ "CONFIDENTIAL" สีแดงโปร่งแสง เอียง 55° ลง `watermarked_document.pdf` |
| 3 | `merge_pdfs` | รวม `dummy_doc1.pdf` + `dummy_doc2.pdf` → `merged_docs.pdf` (2 หน้า) |
| 4 | `extract_word_text` | ดึงข้อความจากรายงาน Word → `extracted_word_text.txt` |
| 5 | `extract_pdf_text` | ดึงข้อความจาก PDF ต้นฉบับ → `extracted_pdf_text.txt` |

## ข้อบกพร่องที่พบและการแก้ไข

โค้ดชุดนี้นำมาจาก GitHub ของผู้สอน ซึ่งแก้ปัญหา relative import ไว้แล้ว
แต่เมื่อนำมารันจริงยังพบอีก 2 จุด

| # | ไฟล์ | อาการ | การแก้ไข |
| --- | --- | --- | --- |
| 1 | `word_tasks.py` | ตารางในรายงานออกมา**ไม่มีเส้นขอบเลย** พร้อม WARNING ว่า `Style 'Table Grid' not available` | เทมเพลต `report_template.docx` มีเฉพาะสไตล์ `Normal Table` ไม่มี `Table Grid` (ซึ่งเทมเพลตมาตรฐานของ python-docx มีให้) โค้ดเดิมดักด้วย try-except แล้วปล่อยผ่าน → เพิ่มฟังก์ชัน `_apply_table_borders()` วาดเส้นขอบเองผ่าน XML เมื่อไม่มีสไตล์ |
| 2 | `utils.py` | ข้อความ log ถูกพิมพ์ซ้ำ 2 บรรทัด (41 บรรทัด) | `basicConfig` ใส่ handler ที่ root แล้ว `setup_logging` ใส่อีกที่ logger ลูก → เพิ่ม `logger.propagate = False` (เหลือ 30 บรรทัด) |

## สิ่งที่ต้องส่ง (ตามโจทย์)

- [x] ส่งเป็น github
- [x] screenshot ไฟล์ `merged_docs.pdf`
- [x] screenshot ไฟล์ `generated_report.docx`
- [x] screenshot ไฟล์ `watermarked_document.pdf`
- [x] แนบภาพไว้กับโปรเจกต์ week 11 (โฟลเดอร์ `screenshots/`)

## แนวทางต่อยอด

* เพิ่ม task type สำหรับแยกไฟล์ PDF (split) และเข้ารหัสด้วยรหัสผ่าน
* ใส่ลายน้ำเป็นรูปภาพ (โลโก้) แทนข้อความ
* สร้างรายงานหลายฉบับพร้อมกันจากข้อมูลหลายชุดใน config เดียว
* ส่งไฟล์ที่สร้างเสร็จออกทางอีเมลอัตโนมัติ (ต่อยอดไปแล็บสัปดาห์ที่ 12)
