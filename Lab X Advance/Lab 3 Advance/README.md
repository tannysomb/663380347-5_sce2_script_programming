# Week 10 — LabX ADV: Advanced Spreadsheet Automation & Agentic Workflows

โปรเจกต์นี้ยกระดับการทำงานกับ Excel จากการเขียนโค้ดสั่งทีละขั้น ไปเป็น **"Spreadsheet Agent"**
ที่อ่านลำดับงานจากไฟล์ configuration แบบ JSON แล้วทำงานตามแผนทีละ task
พร้อมบันทึกทุกขั้นตอนลงชีต **Audit Log** ในไฟล์ผลลัพธ์

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **Config-Driven Automation** — นิยาม pipeline ทั้งหมดใน `configs/example_spreadsheet_config.json` เปลี่ยนงานได้โดยไม่ต้องแก้โค้ด
* **Task Dispatching** — agent อ่าน `type` ของแต่ละ task แล้วเรียกเมธอดที่ตรงกัน
* **openpyxl ขั้นสูง**
  * `copy_data` — คัดลอกข้อมูลข้ามชีต
  * `calculate_column` — ใส่สูตร Excel ลงคอลัมน์ใหม่ (`=B{row}*C{row}`)
  * `conditional_format` — color scale, data bar, icon set และ expression rule
  * `chart` — สร้าง BarChart / LineChart / PieChart พร้อมแกนและหัวข้อ
* **Audit Logging** — ทุก task บันทึกสถานะ (SUCCESS / WARNING / ERROR) พร้อม timestamp ลงชีต Audit Log

## โครงสร้างโปรเจกต์

```text
week10_advanced/
├── src/
│   ├── __init__.py
│   ├── spreadsheet_agent.py     # ตัวควบคุมหลัก: อ่าน task แล้วสั่งงาน openpyxl
│   ├── config_parser.py         # โหลดและตรวจสอบ config
│   ├── utils.py                 # logging และฟังก์ชันช่วย
│   └── google_sheets_utils.py   # โครงสำหรับต่อยอดไป Google Sheets (เชิงแนวคิด)
├── configs/
│   └── example_spreadsheet_config.json
├── data/
│   ├── input_data.xlsx          # ข้อมูลตั้งต้น (ชีตชื่อ SalesData)
│   └── output_report.xlsx       # ผลลัพธ์ 3 ชีต: Audit Log, SalesData, Raw Data
├── screenshots/                 # ภาพผลลัพธ์ตามที่โจทย์กำหนดให้แนบ
├── main.py
├── .gitignore
└── README.md
```

## วิธีรัน

```bash
pip install openpyxl
python main.py
```

> ต้องรันจากในโฟลเดอร์ `week10_advanced` เพราะ config ใช้เส้นทางสัมพัทธ์ (`data/input_data.xlsx`)

Agent จะทำงาน 6 tasks ตามลำดับ:

1. `copy_data` — คัดลอก `SalesData` → ชีตใหม่ `Raw Data`
2. `calculate_column` — ใส่สูตร `=B{row}*C{row}` ในคอลัมน์ D (Total Revenue)
3. `conditional_format` — color scale (แดง→เหลือง→เขียว) บน `D2:D100`
4. `chart` — Bar Chart รายได้ 4 สินค้าแรก วางที่ G2
5. `calculate_column` — ใส่สูตร `=IF(D{row}>1000,"High Value","Standard")` ในคอลัมน์ E
6. `conditional_format` — expression rule ไฮไลต์เขียวเมื่อ Status = "High Value"

จากนั้นสร้างชีต `Audit Log` เป็นชีตแรก แล้วบันทึกเป็น `data/output_report.xlsx`

## บั๊กที่พบในโค้ดต้นฉบับและการแก้ไข

เอกสารแลปให้โค้ดเต็มมา แต่นำมารันตรง ๆ ไม่ได้ พบปัญหา 6 จุด รายละเอียดอยู่ในรายงาน PDF หัวข้อ 4

| # | ไฟล์ | อาการ | การแก้ไข |
| --- | --- | --- | --- |
| 1 | `main.py` | `from .src.utils import` เป็น relative import ใน `__main__` และวางไว้ก่อน `sys.path.append` | ย้าย `sys.path.append` ขึ้นก่อน แล้วเปลี่ยนเป็น `from utils import` |
| 2 | `config_parser.py`, `spreadsheet_agent.py` | `from .utils import` ใช้ไม่ได้กับวิธี `sys.path.append('src')` | เปลี่ยนเป็น absolute import |
| 3 | `config_parser.py` | validator บังคับทุก task ต้องมี `sheet` แต่ `copy_data` ใช้ `source_sheet`/`dest_sheet` → pipeline ไม่เริ่มทำงาน | ยกเว้น `copy_data` ให้ตรวจ `source_sheet`/`dest_sheet` แทน |
| 4 | `spreadsheet_agent.py` | เรียก `json.dumps()` ตอนสร้าง Audit Log แต่ไม่ได้ `import json` | เพิ่ม `import json` |
| 5 | `spreadsheet_agent.py` | conditional format แบบ `expression` เรียก `add(range, ruleType=..., formula=..., dxf=...)` ซึ่งไม่ใช่ API ของ openpyxl | สร้าง `Rule(type="expression", formula=[...], dxf=dxf)` แล้วค่อย `add(range, rule)` |
| 6 | `spreadsheet_agent.py` | สร้างกราฟด้วย `Series(...)` + `chart.series.append()` ทำให้ไม่มีข้อมูลในกราฟ | ใช้ `chart.add_data(data, titles_from_data=True)` ตามแนวทางปกติของ openpyxl |

## ข้อควรรู้เรื่องสูตรใน openpyxl

openpyxl **ไม่มีตัวคำนวณสูตร** — เมื่อเขียน `=B2*C2` ลงเซลล์ ไฟล์จะเก็บเป็น *ข้อความสูตร*
ค่าจริงจะถูกคำนวณเมื่อเปิดไฟล์ด้วย Excel/LibreOffice เท่านั้น
ดังนั้นถ้าอ่านไฟล์กลับด้วย openpyxl จะเห็นเป็น `=B2*C2` ไม่ใช่ `2401`
หากต้องการอ่านค่าที่คำนวณแล้ว ต้องเปิดไฟล์ใน Excel บันทึกทับก่อน แล้วโหลดด้วย `load_workbook(..., data_only=True)`

## สิ่งที่ต้องส่ง (ตามโจทย์)

- [x] link github
- [x] screenshot ชีต Audit Log
- [x] screenshot ชีต SalesData
- [x] screenshot ชีต Raw Data
- [x] รวมภาพไว้ในโฟลเดอร์ `screenshots`

> **หมายเหตุ:** ภาพใน `screenshots/` วาดขึ้นจากข้อมูลจริงในไฟล์ `.xlsx` เพื่อใช้ประกอบรายงาน
> หากต้องการภาพจับหน้าจอ Excel จริง ให้เปิด `data/output_report.xlsx` ด้วย Excel แล้วจับหน้าจอเอง
> ซึ่งจะเห็นค่าที่สูตรคำนวณแล้วและกราฟที่ Excel เรนเดอร์

## แนวทางต่อยอด

* เพิ่ม task type ใหม่ เช่น `add_data_validation` (dropdown), `protect_sheet`
* นำเข้าข้อมูลจาก CSV หรือฐานข้อมูล SQLite แทนการอ่านจาก Excel อย่างเดียว
* เชื่อมต่อ Google Sheets ผ่าน `gspread` (โครงไฟล์เตรียมไว้แล้วใน `google_sheets_utils.py`)
