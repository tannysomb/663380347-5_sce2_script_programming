# Week 8 — LabX ADV: Agentic Data Processing (Advanced CSV & JSON Workflows)

โปรเจกต์นี้ยกระดับการทำงานกับข้อมูล CSV/JSON จากการเรียกฟังก์ชันตรง ๆ ไปเป็น **"Data Agent"**
ที่อ่านลำดับงาน (pipeline) จากไฟล์ configuration แบบ JSON แล้วทำงานตามที่กำหนดทีละขั้น
โดยส่งผลลัพธ์ระหว่างขั้นตอนผ่าน **data store** ภายในตัวเอง

## แนวคิดสำคัญที่สาธิตในโปรเจกต์

* **Agentic Workflow Orchestration** — `DataAgent` อ่าน pipeline จาก `configs/data_pipeline_config.json` แล้วรันทีละ task ตามลำดับ
* **Internal Data Store** — เก็บผลลัพธ์ระหว่างทางไว้ใน `self.data_store` และส่งต่อระหว่าง task ด้วย `input_data_key` / `output_data_key`
* **Advanced CSV** — โหลดด้วย `DictReader`, จัดกลุ่มและรวมยอด (aggregate), กรองข้อมูล, บันทึกด้วย `DictWriter`
* **Advanced JSON** — อัปเดตข้อมูลซ้อนชั้นด้วย dot-notation path, เพิ่ม/ลบสมาชิกใน list, query ข้อมูลเฉพาะจุด
* **Cross-Format Conversion** — แปลง CSV (list of dicts) เป็น JSON พร้อมแปลงชนิดข้อมูลอัตโนมัติ
* **Audit Logging** — บันทึกทุกขั้นตอน (เริ่ม/สำเร็จ/ผิดพลาด) ลงไฟล์ `reports/audit_report_*.json`

## โครงสร้างโปรเจกต์

```text
advanced/
├── src/
│   ├── __init__.py
│   ├── data_agent.py         # ตัวควบคุมหลัก: อ่าน config, สั่งงาน task, จัดการ state
│   ├── csv_tasks.py          # โหลด/บันทึก/รวมยอด/กรอง CSV
│   ├── json_tasks.py         # โหลด/บันทึก/อัปเดต/query JSON
│   ├── conversion_tasks.py   # แปลง CSV <-> JSON
│   ├── config_parser.py      # โหลดและตรวจสอบความถูกต้องของ config
│   └── utils.py              # logging, สร้างโฟลเดอร์, audit log
├── configs/
│   └── data_pipeline_config.json   # นิยาม pipeline ทั้งหมด
├── data/
│   ├── input_sales.csv                  # ข้อมูลตั้งต้น (การขาย 10 รายการ)
│   ├── input_inventory.json             # ข้อมูลตั้งต้น (สินค้า 3 รายการ)
│   ├── processed_sales_by_customer.csv  # ผลลัพธ์: ยอดขายรวมรายลูกค้า
│   ├── sales_data.json                  # ผลลัพธ์: CSV ที่แปลงเป็น JSON
│   └── updated_inventory.json           # ผลลัพธ์: สินค้าคงคลังที่อัปเดตแล้ว
├── reports/
│   └── audit_report_*.json   # รายงานตรวจสอบการทำงานของ agent
├── main.py
├── .gitignore
└── README.md
```

## วิธีรัน

```bash
python main.py
```

Pipeline ที่กำหนดไว้จะทำงาน 9 ขั้นตอนตามลำดับ:

1. โหลด `input_sales.csv` → เก็บใน `raw_sales_data`
2. รวมยอดขายตาม `Customer` → เก็บใน `customer_sales_summary`
3. บันทึกยอดรวมลง `processed_sales_by_customer.csv`
4. แปลงข้อมูลขายดิบเป็น JSON → เก็บใน `raw_sales_json`
5. บันทึกลง `sales_data.json`
6. โหลด `input_inventory.json` → เก็บใน `raw_inventory_data`
7. อัปเดตสต็อก/รายละเอียด และเพิ่มสินค้าใหม่ → เก็บใน `updated_inventory_data`
8. Query ยี่ห้อของสินค้าชิ้นแรก (`0.details.brand`)
9. บันทึกลง `updated_inventory.json` และสร้าง audit report

## โครงสร้างของไฟล์ config

| ฟิลด์ | ความหมาย |
| --- | --- |
| `type` | ชนิดของงาน เช่น `load_csv`, `transform_csv_aggregate`, `save_json` |
| `input_data_key` | คีย์ใน data store ที่จะดึงข้อมูลเข้ามาใช้ |
| `output_data_key` | คีย์ใน data store ที่จะเก็บผลลัพธ์ไว้ (ใช้ต่อ task ถัดไป) |
| `file_path` | เส้นทางไฟล์ สำหรับงานที่อ่าน/เขียนไฟล์ |
| `group_by_field` / `aggregate_field` / `aggregate_type` | พารามิเตอร์ของการรวมยอด CSV |
| `updates` | รายการคำสั่งแก้ไข JSON แต่ละรายการมี `path`, `value`, `operation` |
| `path` | เส้นทางแบบ dot-notation เช่น `0.details.brand` |

## บั๊กที่พบในโค้ดต้นฉบับและการแก้ไข

ระหว่างนำโค้ดจากเอกสารประกอบการสอนมารันจริง พบข้อผิดพลาด 6 จุดที่ทำให้โปรแกรมทำงานไม่ได้
หรือทำงานไม่ครบตามที่โจทย์กำหนด รายละเอียดทั้งหมดอยู่ในรายงาน PDF หัวข้อที่ 5

| # | ไฟล์ | อาการ | การแก้ไข |
| --- | --- | --- | --- |
| 1 | `src/*.py` (5 ไฟล์) | `ImportError: attempted relative import` | เปลี่ยน `from .utils import` เป็น `from utils import` |
| 2 | `config_parser.py` | pipeline หยุดที่ task 2 เพราะบังคับให้ทุก task มี `output_data_key` | ยกเว้น task `save_*` ให้ต้องการแค่ `input_data_key` |
| 3 | `data_agent.py` | `NameError: name 'sys' is not defined` | เพิ่ม `import sys` |
| 4 | `json_tasks.py` | `add_to_list` ที่ path ว่างถูกข้าม ทำให้เพิ่มสินค้าใหม่ไม่สำเร็จ | รองรับการเพิ่มสมาชิกเข้า list ที่เป็นรากของข้อมูล |
| 5 | `data_pipeline_config.json` | path `PROD001.details.color` ใช้ไม่ได้เพราะข้อมูลเป็น list | เปลี่ยนเป็น `0.details.color` |
| 6 | `utils.py` | log ถูกพิมพ์ซ้ำ 2 บรรทัด | เพิ่ม `logger.propagate = False` |

## การแก้ปัญหาที่พบบ่อย

* **`FileNotFoundError`** — ตรวจสอบว่ามี `input_sales.csv` และ `input_inventory.json` ในโฟลเดอร์ `data/`
* **`KeyError`** — ตรวจว่าชื่อคอลัมน์ใน CSV และ key ใน JSON ตรงกับที่ config อ้างถึง
* **ข้อมูลไม่เปลี่ยนตามที่คาด** — ตรวจว่า `output_data_key` ของ task ก่อนหน้าตรงกับ `input_data_key` ของ task ถัดไป
* **path ของ JSON ไม่ทำงาน** — ถ้าข้อมูลชั้นนอกเป็น list ต้องอ้างด้วยเลข index (`0`, `1`, `2`) ไม่ใช่ชื่อ id
* **ตรวจสอบย้อนหลัง** — เปิดไฟล์ `reports/audit_report_*.json` เพื่อดูสถานะของทุก task

## แนวทางต่อยอด

* รองรับการ join/merge ข้อมูลจากหลายไฟล์ CSV
* ตรวจสอบความถูกต้องของข้อมูลด้วย `jsonschema`
* เพิ่มการทำงานแบบมีเงื่อนไข (รัน task ถัดไปเฉพาะเมื่อ task ก่อนหน้าสำเร็จ)
* ดึงข้อมูลจาก Web API หรือฐานข้อมูลแทนการอ่านจากไฟล์
