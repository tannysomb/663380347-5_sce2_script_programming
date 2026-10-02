# Week 12 — LabX ADV: Agentic Communication Workflows (Advanced Email & SMS)

**Agentic Communication Automator** — ยกระดับจากแล็บ Basic โดยเปลี่ยนจากการเขียนโค้ดสั่งส่งอีเมลทีละคำสั่ง
มาเป็น **agent ที่อ่านแผนงานจากไฟล์ configuration** แล้วทำงานตามลำดับ ทั้งส่งอีเมลจากเทมเพลต
ประมวลผลกล่องจดหมายขาเข้า และตอบกลับอัตโนมัติตามเงื่อนไข

## ⚠️ สิ่งที่ต้องทำเองก่อนรัน

โปรแกรมนี้**ส่งอีเมลจริง** จึงต้องใช้บัญชีและรหัสผ่านของคุณเอง ซึ่งผู้ช่วย AI ไม่สามารถกรอกแทนได้

1. คัดลอก `.env.example` เป็น `.env` แล้วกรอก `SENDER_EMAIL` และ `SENDER_APP_PASSWORD` (App Password 16 หลัก)
2. แก้ไฟล์ `configs/comm_pipeline_config.json` เปลี่ยน `your_gmail_address@gmail.com`
   และ `your_test_email@example.com` เป็นอีเมลจริงของคุณ

> 🔒 ไฟล์ `.env` ถูกกันไว้ใน `.gitignore` แล้ว **ห้าม commit ขึ้น GitHub เด็ดขาด**

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **Config-Driven Communication Pipeline** — นิยามงานสื่อสารทั้งหมดใน JSON
* **Template Rendering** — หัวข้อและเนื้อหาอีเมลเป็นเทมเพลตที่เติมค่าได้ เช่น
  `"Daily Sales Report - {report_date}"` และ `"Total sales: ${sales_figure:.2f}"`
* **Inbox Processing** — ค้นหาอีเมลขาเข้าตามเงื่อนไข (ยังไม่อ่าน / ผู้ส่ง / คำในหัวข้อ) แล้วดำเนินการต่อ
* **Conditional Auto-Reply** — ตอบกลับอัตโนมัติเมื่อเจออีเมลที่ตรงเงื่อนไข
* **Audit Logging** — บันทึกทุกขั้นตอนไว้ตรวจสอบย้อนหลัง

## โครงสร้างโปรเจกต์

```text
week12_advanced/
├── src/
│   ├── __init__.py
│   ├── communication_agent.py   # ตัวควบคุมหลัก อ่าน config แล้วสั่งงานทีละ task
│   ├── config_parser.py         # โหลดและตรวจสอบ config
│   ├── email_tasks.py           # ส่งอีเมล / ประมวลผลกล่องจดหมาย
│   ├── sms_tasks.py             # ส่ง SMS ผ่าน gateway
│   ├── template_renderer.py     # เติมค่าลงเทมเพลตหัวข้อและเนื้อหา
│   └── utils.py                 # logging, audit log, อ่านตัวแปรสภาพแวดล้อม
├── configs/
│   └── comm_pipeline_config.json
├── data/
│   ├── reports/                 # ไฟล์แนบ (sales_report.pdf, summary_data.xlsx)
│   └── incoming_attachments/    # ไฟล์แนบที่ดาวน์โหลดจากกล่องจดหมาย
├── screenshots/
├── main.py
├── .env.example
└── README.md
```

## วิธีรัน

```bash
pip install python-dotenv
copy .env.example .env
# แก้ .env และ configs/comm_pipeline_config.json ก่อน
python main.py
```

## ข้อบกพร่องที่พบและการแก้ไข

| # | ไฟล์ | อาการ | การแก้ไข |
| --- | --- | --- | --- |
| 1 | `main.py` | เมื่อยังไม่ได้ตั้งค่า `.env` โปรแกรม**โยน traceback ดิบ**ออกมาทั้งก้อน ซึ่งผู้ใช้อ่านไม่รู้เรื่องว่าต้องทำอะไร (ต่างจากเวอร์ชัน BASIC ที่แจ้งข้อความชัดเจน) | เพิ่มการดัก `ValueError` และ `FileNotFoundError` แยกจาก `Exception` ทั่วไป พร้อมข้อความบอกวิธีแก้ |
| 2 | `utils.py` | ข้อความ log ถูกพิมพ์ซ้ำ 2 บรรทัด | เพิ่ม `logger.propagate = False` |
| 3 | — | `config` อ้างถึงไฟล์แนบ `data/reports/sales_report.pdf` และ `summary_data.xlsx` ที่ไม่มีอยู่จริงใน repo | สร้างไฟล์ตัวอย่างทั้งสองให้ เพื่อให้ pipeline ทำงานได้ครบทันทีที่ใส่ credential |

## การตรวจสอบความถูกต้องของโค้ด

เนื่องจากต้องใช้ credential ส่วนตัวในการส่งอีเมลจริง จึงตรวจสอบเท่าที่ทำได้โดยไม่ต้องใช้บัญชีจริง:

* **Syntax check** — ทุกไฟล์ใน `src/` และ `main.py` คอมไพล์ผ่าน ไม่มี syntax error
* **Config validation** — agent โหลดและตรวจสอบ `comm_pipeline_config.json` ผ่านเรียบร้อย
  (เห็นข้อความ `Configuration validated.` ในภาพผลการรัน)
* **การจัดการเมื่อขาด credential** — หลังแก้บั๊กที่ 1 โปรแกรมแจ้งข้อความชัดเจนแทน traceback ดิบ

ภาพผลการทดสอบอยู่ในโฟลเดอร์ `screenshots/`

## สิ่งที่ต้องส่ง (ตามโจทย์)

- [x] link github
- [ ] **ภาพ screenshot จากอีเมล** → ต้องรันเองหลังตั้งค่า `.env` แล้วจับภาพกล่องจดหมาย

## แนวทางต่อยอด

* ใช้ Twilio API ส่ง SMS จริงแทน email-to-SMS gateway
* เพิ่มเงื่อนไขการตอบกลับที่ซับซ้อนขึ้น เช่น แยกตามคำสำคัญหลายคำ
* ตั้งเวลาให้ agent ทำงานอัตโนมัติทุกวันด้วย Task Scheduler
* สร้างรายงานสรุปอีเมลที่ประมวลผลในแต่ละรอบ
