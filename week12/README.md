# Week 12 — LabX BASIC: Automating Communications (Email & SMS)

โปรเจกต์ **email-sms-automator** สาธิตการส่งอีเมล ส่งอีเมลพร้อมไฟล์แนบ ส่ง SMS ผ่าน carrier gateway
และอ่าน/ดาวน์โหลดไฟล์แนบจากกล่องจดหมายขาเข้า ด้วยไลบรารีมาตรฐานของ Python (`smtplib`, `imaplib`, `email`)

## ⚠️ สิ่งที่ต้องทำเองก่อนรัน

โปรแกรมนี้**ส่งอีเมลจริง** จึงต้องใช้บัญชีและรหัสผ่านของคุณเอง ซึ่งผู้ช่วย AI ไม่สามารถกรอกแทนได้

1. คัดลอก `.env.example` เป็น `.env`
   ```bash
   copy .env.example .env
   ```
2. เปิดไฟล์ `.env` แล้วกรอกค่าให้ครบ โดยเฉพาะ
   * `SENDER_EMAIL` — อีเมล Gmail ของคุณ
   * `SENDER_APP_PASSWORD` — **App Password 16 หลัก** (ไม่ใช่รหัสผ่านที่ใช้ล็อกอินปกติ)
   * `TEST_RECIPIENT_EMAIL` — อีเมลปลายทางสำหรับทดสอบ
3. วิธีสร้าง App Password: Google Account → Security → เปิด 2-Step Verification ก่อน → App passwords → สร้างใหม่

> 🔒 ไฟล์ `.env` ถูกกันไว้ใน `.gitignore` แล้ว **ห้าม commit ขึ้น GitHub เด็ดขาด**

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **ส่งอีเมล (SMTP)** — `smtplib.SMTP()` + `starttls()` + `login()` + `send_message()`
* **อีเมลพร้อมไฟล์แนบ** — ประกอบข้อความด้วย `EmailMessage` แล้ว `add_attachment()`
* **ส่ง SMS ผ่าน Email-to-SMS Gateway** — ส่งอีเมลไปยัง `เบอร์โทร@gateway-ของค่าย` เช่น `1234567890@txt.att.net`
* **รับอีเมล (IMAP)** — `imaplib.IMAP4_SSL()` ค้นหาอีเมลด้วยเงื่อนไข แล้วดาวน์โหลดไฟล์แนบ
* **จัดการ credential อย่างปลอดภัย** — อ่านจากไฟล์ `.env` ผ่าน `python-dotenv` ไม่ฝังไว้ในโค้ด

## โครงสร้างโปรเจกต์

```text
week12/
├── src/
│   ├── __init__.py
│   ├── email_sender.py      # ส่งอีเมลธรรมดาและแบบมีไฟล์แนบ
│   ├── email_receiver.py    # อ่านกล่องจดหมายและดาวน์โหลดไฟล์แนบ
│   ├── sms_gateway.py       # ส่ง SMS ผ่าน email-to-SMS gateway
│   └── utils.py             # logging และการอ่านตัวแปรสภาพแวดล้อม
├── data/
│   ├── dummy_report.pdf     # ไฟล์แนบตัวอย่าง
│   └── attachments/         # ปลายทางของไฟล์แนบที่ดาวน์โหลดมา
├── tests/
│   └── test_automator.py    # ชุดทดสอบ 18 รายการ
├── screenshots/
├── main.py
├── .env.example             # เทมเพลตการตั้งค่า (คัดลอกเป็น .env)
├── .gitignore
├── requirements.txt
└── README.md
```

## วิธีรัน

```bash
pip install -r requirements.txt
copy .env.example .env
# แก้ไข .env ใส่ค่าจริงก่อน
python main.py
```

## การตรวจสอบความถูกต้องของโค้ด

เนื่องจากการส่งอีเมลจริงต้องใช้ credential ส่วนตัว จึงตรวจสอบโค้ดด้วยวิธีที่ไม่ต้องใช้บัญชีจริง 2 แบบ

**1. ชุดทดสอบอัตโนมัติ — ผ่านทั้ง 18 รายการ**

```bash
python -m pytest tests/ -v
# 18 passed
```

**2. ทดสอบการจัดการเมื่อยังไม่ได้ตั้งค่า `.env`**

เมื่อรันโดยไม่มีไฟล์ `.env` โปรแกรมแจ้งข้อความชัดเจนว่าตัวแปรใดขาดไป แล้วจบการทำงานอย่างเรียบร้อย
ไม่โยน traceback ดิบใส่ผู้ใช้

```text
CRITICAL - Configuration error: Environment variable 'SENDER_EMAIL' not set.
Please check your .env file or environment settings.
```

ภาพผลการทดสอบทั้งสองแบบอยู่ในโฟลเดอร์ `screenshots/`

## สิ่งที่ต้องส่ง (ตามโจทย์)

- [x] link github
- [ ] **ภาพ screenshot แจ้งเตือน email จากการรันโค้ด** โดยเนื้อหาเป็น ชื่อ นามสกุล รหัสนักศึกษา
      → ต้องรันเองหลังตั้งค่า `.env` แล้วจับภาพกล่องจดหมาย
- หมายเหตุจากโจทย์: Task 3 ที่เป็นการส่ง SMS หากส่งไม่ได้ไม่เป็นไร

> 💡 **แนะนำ:** แก้หัวข้อ/เนื้อหาอีเมลใน `main.py` ให้มี ชื่อ-นามสกุล และรหัสนักศึกษาของคุณ
> ก่อนรัน เพื่อให้ภาพ screenshot ตรงตามที่โจทย์กำหนด

## การแก้ปัญหาที่พบบ่อย

| ปัญหา | สาเหตุ | วิธีแก้ |
| --- | --- | --- |
| `SMTPAuthenticationError` | ใช้รหัสผ่านปกติแทน App Password หรือยังไม่ได้เปิด 2-Step Verification | สร้าง App Password 16 หลักแล้วใช้ค่านั้นแทน |
| `Environment variable not set` | ยังไม่ได้สร้างไฟล์ `.env` หรือกรอกไม่ครบ | คัดลอกจาก `.env.example` แล้วกรอกให้ครบทุกบรรทัด |
| SMS ไม่ถึงปลายทาง | ค่ายมือถือไทยส่วนใหญ่ไม่รองรับ email-to-SMS gateway ซึ่งเป็นบริการของค่ายในสหรัฐฯ | เป็นเรื่องปกติ โจทย์ระบุว่าหากส่งไม่ได้ไม่เป็นไร |
| อีเมลเข้าโฟลเดอร์ Spam | ผู้รับยังไม่เคยติดต่อกับผู้ส่ง | ตรวจในโฟลเดอร์ Spam แล้วกด Not Spam |

## แนวทางต่อยอด

* ส่งอีเมลแบบ HTML พร้อมรูปภาพฝังในเนื้อหา
* ตั้งเวลาส่งอัตโนมัติด้วย `schedule` หรือ Task Scheduler
* ใช้บริการ SMS จริงอย่าง Twilio แทน email-to-SMS gateway
* ตอบกลับอีเมลอัตโนมัติตามคำสำคัญในหัวข้อ
