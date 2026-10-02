# Week 11 — LabX BASIC: Automating PDFs & Word Documents

โปรเจกต์นี้สาธิตการทำงานกับเอกสาร PDF และ Word ด้วย Python โดยใช้ **PyPDF2** สำหรับ PDF
และ **python-docx** สำหรับไฟล์ Word

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **ดึงข้อความจาก PDF** — `PdfReader` + `page.extract_text()`
* **รวมไฟล์ PDF** — `PdfWriter` นำหน้าจากหลายไฟล์มาต่อกันเป็นไฟล์เดียว
* **แยกไฟล์ PDF** — ตัดไฟล์เป็นชิ้นย่อยตามจำนวนหน้าที่กำหนด
* **สร้างเอกสาร Word** — หัวข้อ ย่อหน้า การจัดรูปแบบ (ตัวหนา ตัวเอียง ขนาดฟอนต์ การจัดวาง) และตาราง
* **การออกแบบแบบโมดูล** — แยก `pdf_processor.py` กับ `word_processor.py` ออกจากกันชัดเจน

## โครงสร้างโปรเจกต์

```text
week11/
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py     # ดึงข้อความ / รวม / แยก PDF
│   ├── word_processor.py    # สร้างและจัดรูปแบบเอกสาร Word
│   └── utils.py             # logging และการสร้างโฟลเดอร์
├── documents/
│   ├── input_article.pdf        # PDF ตั้งต้นสำหรับดึงข้อความ (2 หน้า)
│   ├── dummy_doc1.pdf           # PDF สำหรับทดสอบการรวมไฟล์
│   ├── dummy_doc2.pdf
│   ├── output_report.docx       # ผลลัพธ์: รายงาน Word
│   └── merged_output.pdf        # ผลลัพธ์: PDF ที่รวมแล้ว (2 หน้า)
├── screenshots/             # ภาพผลลัพธ์ตามที่โจทย์กำหนดให้แนบ
├── main.py
├── .gitignore
└── README.md
```

## การติดตั้งและวิธีรัน

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install PyPDF2 python-docx
python main.py
```

โปรแกรมทำงาน 2 งานหลัก:

**Task 1 — PDF → Word**
1. ดึงข้อความจาก `input_article.pdf` (2 หน้า) โดยคั่นแต่ละหน้าด้วย `--- Page End ---`
2. สร้างเอกสาร Word ใหม่ ใส่หัวข้อ `Automated Document Report`
3. ใส่ย่อหน้าตัวหนา ย่อหน้าตัวเอียงจัดกลาง และข้อความที่ดึงมาจาก PDF
4. ใส่หัวข้อย่อย `Summary Data` พร้อมตารางสรุป 4 แถว
5. บันทึกเป็น `output_report.docx`

**Task 2 — รวม PDF**
รวม `dummy_doc1.pdf` + `dummy_doc2.pdf` เป็น `merged_output.pdf` (ได้ 2 หน้า)

## ผลลัพธ์ที่ได้

ตารางสรุปใน `output_report.docx`:

| Metric | Value | Notes |
| --- | --- | --- |
| Total Pages Processed | 2 | From Input PDF |
| Document Type | PDF/Word Hybrid | |
| Generated Date | (วันที่ที่รัน) | |

ค่า `Total Pages Processed` มาจากการนับจำนวนตัวคั่น `--- Page End ---` ในข้อความที่ดึงมา
ซึ่งได้ 2 ตรงกับจำนวนหน้าจริงของ `input_article.pdf`

## บั๊กที่พบในโค้ดต้นฉบับและการแก้ไข

| # | ไฟล์ | อาการ | การแก้ไข |
| --- | --- | --- | --- |
| 1 | `pdf_processor.py` | `SyntaxError` — เมธอด `split_pdf` เขียน `range(0_int, total_pages, ...)` ซึ่ง `0_int` ไม่ใช่ไวยากรณ์ Python ทำให้ **ไฟล์ทั้งไฟล์ import ไม่ได้** | แก้เป็น `range(0, total_pages, ...)` |
| 2 | `pdf_processor.py` | `split_pdf` เรียก `ensure_directory_exists()` แต่ import มาเฉพาะ `setup_logging` | import `ensure_directory_exists` เพิ่ม |
| 3 | `pdf_processor.py`, `word_processor.py` | `from .utils import` ใช้ไม่ได้กับวิธี `sys.path.append('src')` ของ `main.py` | เปลี่ยนเป็น absolute import |
| 4 | `main.py` | `import datetime` ถูกวางไว้ใน `if __name__ == "__main__":` ทำให้ `main()` พังทันทีถ้าถูก import จากไฟล์อื่น | ย้าย `import datetime` ขึ้นไปบนสุดของไฟล์ |
| 5 | `utils.py` | ข้อความ log ถูกพิมพ์ซ้ำ 2 บรรทัด (`basicConfig` + handler ของ logger ลูก) | เพิ่ม `logger.propagate = False` |

## การแก้ปัญหาที่พบบ่อย

* **`FileNotFoundError`** — ตรวจว่าไฟล์ PDF ตั้งต้นอยู่ในโฟลเดอร์ `documents/` ครบทั้ง 3 ไฟล์
* **ดึงข้อความจาก PDF ได้ว่างเปล่า** — PDF ที่เป็นภาพสแกนจะดึงข้อความไม่ได้ ต้องใช้ OCR แทน
* **`PdfReadError`** — ไฟล์ PDF เสียหายหรือถูกเข้ารหัสไว้
* **ตารางใน Word ไม่มีเส้น** — ต้องกำหนด `table.style = 'Table Grid'`

## สิ่งที่ต้องส่ง (ตามโจทย์)

- [x] ส่งเป็น github
- [x] screenshot ไฟล์ `merged_output.pdf`
- [x] screenshot ไฟล์ `output_report.docx`
- [x] แนบภาพไว้กับโปรเจกต์ week 11 (อยู่ในโฟลเดอร์ `screenshots/`)

## แนวทางต่อยอด

* ใส่ลายน้ำ (watermark) ลงใน PDF
* เข้ารหัส/ถอดรหัส PDF ด้วยรหัสผ่าน
* ใช้ OCR (`pytesseract`) อ่านข้อความจาก PDF ที่เป็นภาพสแกน
* แปลง Word กลับเป็น PDF อัตโนมัติ
