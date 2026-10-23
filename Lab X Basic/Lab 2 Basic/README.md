# Week 8 — LabX BASIC: Automating with CSV and JSON Data

โปรเจกต์นี้ฝึกการทำงานกับไฟล์ข้อมูลแบบมีโครงสร้าง 2 รูปแบบที่ใช้บ่อยที่สุด คือ **CSV** (Comma Separated Values)
และ **JSON** (JavaScript Object Notation) ด้วยโมดูลมาตรฐานของ Python (`csv` และ `json`)

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **อ่าน CSV ด้วย `csv.DictReader`** — อ่านไฟล์ CSV โดยใช้แถวแรกเป็นหัวตาราง แล้วเข้าถึงข้อมูลแบบ dictionary
* **เขียน CSV ด้วย `csv.DictWriter`** — เขียน list ของ dictionary กลับลงไฟล์ CSV พร้อมหัวตารางที่ถูกต้อง
* **ประมวลผลข้อมูล CSV** — รวมยอดขาย หาค่าเฉลี่ยราคา และกรองข้อมูลตามเงื่อนไข
* **อ่าน JSON ด้วย `json.load`** — แปลงไฟล์ JSON เป็น dictionary/list ของ Python
* **เขียน JSON ด้วย `json.dump`** — แปลงอ็อบเจกต์ Python กลับเป็น JSON พร้อมจัดรูปแบบให้อ่านง่าย (`indent`)
* **จัดการข้อมูลซ้อนชั้นใน JSON** — เข้าถึงข้อมูลที่ซ้อนกัน แก้ไขข้อมูลเดิม และเพิ่มข้อมูลใหม่
* **การออกแบบแบบโมดูล** — แยกตรรกะ CSV และ JSON ออกเป็นคนละไฟล์ (`csv_handler.py`, `json_handler.py`)
* **ความแข็งแรงของโปรแกรม** — มี error handling และ logging ในทุกขั้นตอนสำคัญ

## โครงสร้างโปรเจกต์

```text
basic/
├── src/
│   ├── __init__.py          # ทำให้ 'src' เป็น Python package
│   ├── csv_handler.py       # รวมการทำงานเกี่ยวกับ CSV
│   ├── json_handler.py      # รวมการทำงานเกี่ยวกับ JSON
│   └── utils.py             # logging และการสร้างโฟลเดอร์
├── data/
│   ├── input_sales.csv                # ไฟล์ CSV ตั้งต้น (ข้อมูลการขาย)
│   ├── input_inventory.json           # ไฟล์ JSON ตั้งต้น (ข้อมูลสินค้าคงคลัง)
│   ├── output_filtered_sales.csv      # ผลลัพธ์: CSV ที่กรองแล้ว + แถวสรุป
│   └── output_updated_inventory.json  # ผลลัพธ์: JSON ที่อัปเดตแล้ว
├── main.py                  # จุดเริ่มต้นของโปรแกรม
├── .gitignore
└── README.md
```

## วิธีรัน

```bash
python main.py
```

โปรแกรมจะทำงานตามลำดับนี้:

1. อ่าน `data/input_sales.csv`
2. ประมวลผลข้อมูลการขาย กรองเฉพาะรายการที่ `Amount` >= 100 พร้อมคำนวณยอดรวมและค่าเฉลี่ย
3. เขียนผลลัพธ์ที่กรองแล้ว (พร้อมแถว SUMMARY) ลง `data/output_filtered_sales.csv`
4. อ่าน `data/input_inventory.json`
5. อัปเดตจำนวนสต็อกของ `PROD001` และ `PROD003`
6. เพิ่มสินค้าใหม่ `PROD004` (Gaming Headset)
7. เขียนข้อมูลที่อัปเดตแล้วลง `data/output_updated_inventory.json`

## การแก้ปัญหาที่พบบ่อย

| ปัญหา | สาเหตุ | วิธีแก้ |
| --- | --- | --- |
| `FileNotFoundError` | ไฟล์ตั้งต้นไม่อยู่ในโฟลเดอร์ `data/` | ตรวจสอบว่ามี `input_sales.csv` และ `input_inventory.json` อยู่จริง |
| `KeyError` | ชื่อหัวตารางใน CSV ไม่ตรงกับ key ที่เรียกใช้ | ตรวจสอบตัวสะกดและช่องว่างหน้า-หลังชื่อคอลัมน์ |
| `json.JSONDecodeError` | ไวยากรณ์ JSON ผิด | ตรวจสอบเครื่องหมายจุลภาค วงเล็บ และเครื่องหมายคำพูดให้ครบถ้วน |
| `ValueError: could not convert string to float` | คอลัมน์ตัวเลขมีอักขระที่ไม่ใช่ตัวเลข (เช่น `$`, `,`) | ทำความสะอาดข้อมูลก่อนแปลงเป็น `float()` |
| ตัวอักษรเพี้ยนในไฟล์ผลลัพธ์ | encoding ไม่ตรงกัน | ใช้ `encoding='utf-8'` ทั้งตอนอ่านและเขียน |

## แนวทางต่อยอด

* เขียนตัวแปลงข้อมูลระหว่าง CSV และ JSON (CSV-to-JSON / JSON-to-CSV)
* เพิ่มการตรวจสอบความถูกต้องของข้อมูล (data validation) ให้เข้มงวดขึ้น
* รองรับไฟล์ขนาดใหญ่ด้วยการอ่านเป็น chunk หรือใช้ `pandas` / `ijson`
* ดึงข้อมูล JSON จาก Web API จริงมาประมวลผลต่อ
* ใช้ CSV/JSON เป็นตัวกลางนำเข้า-ส่งออกข้อมูลกับฐานข้อมูล เช่น SQLite
