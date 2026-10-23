นี่คือเนื้อหาทั้งหมดที่ถูกจัดรูปแบบใหม่ให้เรียบร้อย สวยงาม อ่านง่าย เป็นสัดส่วนด้วย Markdown โดย **ไม่ตัดทอนหรือดัดแปลงเนื้อหาเดิม** ครับ

---

# บทเรียน: Agentic Web Scraper ด้วย Python และ Selenium

## 📌 ภาพรวม

สัปดาห์นี้เราจะก้าวข้ามการทำ web scraping แบบพื้นฐาน ไปสู่เทคนิคขั้นสูง ซึ่งรวมถึงการจัดการเนื้อหาเว็บแบบไดนามิก (dynamic web content) และการแนะนำแนวคิดพื้นฐานของ **"agentic AI"** ในงานอัตโนมัติ นักศึกษาจะได้เรียนรู้การสร้าง scraper ที่แข็งแรงและปรับตัวได้มากขึ้น ซึ่งสามารถทำงานตามคำสั่งจากไฟล์ configuration ได้ เสมือนเป็นการจำลอง autonomous agent

---

## 🎯 ผลลัพธ์การเรียนรู้ / การประเมินคุณลักษณะ

* เชี่ยวชาญเทคนิค web scraping ขั้นสูง โดยเฉพาะเนื้อหาที่ต้องเรนเดอร์ด้วย JavaScript โดยใช้ Selenium
* นำ error handling, retry mechanism และกลยุทธ์ anti-blocking ขั้นพื้นฐานมาใช้
* ออกแบบและใช้ไฟล์ configuration เพื่อกำหนดพฤติกรรมการ scrape เลียนแบบแนวทาง "agentic"
* เข้าใจการจัดโครงสร้างข้อมูลที่ scrape มา และจัดเก็บในรูปแบบต่าง ๆ
* วิเคราะห์โครงสร้างหน้าเว็บที่ซับซ้อน และเขียน CSS selector หรือ XPath ที่มีประสิทธิภาพ
* เข้าใจความรับผิดชอบด้านจริยธรรมและกฎหมายที่เกี่ยวข้องกับการ scraping แบบอัตโนมัติขั้นสูง

> **การประเมินคุณลักษณะ:** การแก้ปัญหาขั้นสูง, การออกแบบระบบ, วิศวกรรมความแข็งแรงของระบบ (robustness), การจัดการ configuration, การตัดสินใจเชิงจริยธรรมในงานอัตโนมัติ, พื้นฐานความคิดแบบ AI

---

## 📚 รายละเอียดเนื้อหาบทเรียน

### 1. ทบทวนและข้อจำกัดของการ Scraping แบบพื้นฐาน

* ทบทวน `requests` + `BeautifulSoup` สำหรับ HTML แบบ static
* **ข้อจำกัด:** จะเกิดอะไรขึ้นเมื่อเจอเนื้อหาที่โหลดด้วย JavaScript, infinite scrolling, หรือการคลิกปุ่ม?

### 2. การ Scrape เนื้อหาไดนามิกด้วย Selenium

* **แนะนำ Selenium:** คืออะไร ทำงานอย่างไร (browser automation), แนวคิด WebDriver
* **การติดตั้ง:** `pip install selenium`, การดาวน์โหลดและตั้งค่า WebDriver ตามเบราว์เซอร์ (เช่น ChromeDriver, GeckoDriver)
* **การควบคุมเบราว์เซอร์พื้นฐาน:** เปิดเบราว์เซอร์, นำทาง URL (`driver.get()`), ปิด
* **การค้นหา Element:** `find_element(By.ID, "id")`, `find_element(By.CSS_SELECTOR, "css selector")`, `find_element(By.XPATH, "xpath")`
* **การโต้ตอบกับ Element:** คลิกปุ่ม (`.click()`), พิมพ์ข้อความ (`.send_keys()`), ดึงข้อความ (`.text`)
* **กลยุทธ์การรอ (Waiting Strategies):**
* *Implicit Waits* — timeout แบบทั่วไปสำหรับการค้นหา element
* *Explicit Waits* (`WebDriverWait`, `EC`) — รอเงื่อนไขเฉพาะ (เช่น element คลิกได้ มองเห็นได้) สำคัญมากสำหรับเนื้อหาไดนามิก


* **Headless Browsers:** การรันเบราว์เซอร์แบบไม่มี UI เพื่อเพิ่มประสิทธิภาพ (`--headless`)

### 3. กลยุทธ์ความแข็งแรงของระบบและการป้องกันการถูกบล็อก

* **Delays:** ใช้ `time.sleep()` สำหรับการหน่วงพื้นฐาน แต่แนะนำให้ใช้ explicit waits เพื่อความน่าเชื่อถือที่ดีกว่า
* **User-Agent Spoofing:** ตั้งค่า User-Agent แบบกำหนดเองใน Selenium options
* **Retry Mechanisms พื้นฐาน:** ใช้ loop กับ `try-except` สำหรับข้อผิดพลาดชั่วคราว
* **IP Rotation (แนวคิด):** กล่าวถึง proxy และ VPN โดยสังเขป (ซับซ้อนเกินระดับนี้)

### 4. การจัดโครงสร้างและการจัดเก็บข้อมูล

* กำหนด Python class หรือ dictionary เพื่อแสดงข้อมูลที่ scrape มา (เช่น Product ที่มี name, price, description)
* บันทึกข้อมูลที่จัดโครงสร้างแล้วเป็นไฟล์ CSV (ใช้ `csv` module) และ JSON (ใช้ `json` module)

### 5. แนะนำแนวคิดการ Scraping แบบ "Agentic"

* **Agent คืออะไร?** นิยาม: มีเป้าหมาย, รับรู้สภาพแวดล้อม, ดำเนินการ, ปรับตัวได้
* **Configuration-Driven Agents:** จำลองพฤติกรรมแบบ agent โดยกำหนดกฎ (แผน) ในไฟล์ configuration
* **การกำหนด "กฎ" การ scraping (`.json` config):**
* `start_url`
* `pagination_selector` (CSS/XPath สำหรับปุ่ม/ลิงก์ "หน้าถัดไป")
* `item_container_selector` (selector สำหรับบล็อกสินค้า/บทความหนึ่งรายการ)
* `item_data_selectors` (dictionary ของ selector สำหรับฟิลด์ต่าง ๆ: name_selector, price_selector, description_selector)


* **Automation Loop:** agent (scraper ของคุณ) อ่าน config, นำทาง, ดึงข้อมูล, หาหน้าถัดไป, ทำซ้ำจนไม่มีหน้าเหลือ

### 6. เจาะลึกจริยธรรมและกฎหมายสำหรับการ Scraping ขั้นสูง

* ย้ำเรื่อง `robots.txt` และ Terms of Service
* ความเสี่ยงจากการถูกบล็อก IP, การถูกดำเนินคดี (จดหมาย Cease and Desist)
* ความสำคัญของ rate limiting และการ scrape อย่างมีความรับผิดชอบ
* เจ้าของเว็บไซต์อาจมองการใช้ Selenium แตกต่างออกไปอย่างไร

---

## 🤖 ต้นแบบ: Config-Driven Product Scraper Agent

เราจะสร้าง **"Agentic Product Scraper"** ที่อ่านไฟล์ configuration เพื่อ scrape ข้อมูลสินค้าจากหน้ารายการสินค้าอีคอมเมิร์ซ (สมมติหรือหน้าสาธารณะที่เรียบง่ายมาก) จัดการ pagination และบันทึกข้อมูล

> **หมายเหตุ:** เพื่อการสาธิต เราจะสมมติโครงสร้างเว็บไซต์เป้าหมายแบบง่าย การใช้เว็บไซต์เชิงพาณิชย์ที่ซับซ้อนและใช้งานจริงอาจนำไปสู่การถูกบล็อกหรือปัญหาทางกฎหมาย แนะนำให้ใช้ mock site หรือหน้า directory สาธารณะที่เรียบง่ายมากสำหรับแบบฝึกหัดของนักศึกษา เราจะใช้ `example_site_config.json` ที่เป็นแนวคิดซึ่งอธิบายโครงสร้างหน้าอีคอมเมิร์ซโดยทั่วไป

### 🎯 เป้าหมายของ Agent

1. อ่าน configuration ที่เฉพาะเจาะจงกับไซต์
2. นำทางไปยัง URL เริ่มต้น
3. ดึงรายละเอียดสินค้าที่กำหนดไว้ล่วงหน้าจากหน้าปัจจุบัน
4. ค้นหาและคลิกปุ่ม/ลิงก์ "หน้าถัดไป"
5. ทำซ้ำจนไม่พบหน้าเพิ่มเติม หรือถึงขีดจำกัดที่กำหนด
6. บันทึกข้อมูลทั้งหมดที่ดึงมาลงไฟล์ JSON

### 🔑 เนื้อหาสำคัญ

* **แนวคิดหลักที่สาธิต:**
* Selenium สำหรับเนื้อหาไดนามิก
* การจัดการ WebDriver อัตโนมัติด้วย `webdriver_manager`
* Config-Driven Automation — พฤติกรรมของ scraper กำหนดในไฟล์ JSON ภายนอก
* การออกแบบ Agent แบบโมดูล
* ความแข็งแรงของระบบ (Robustness)
* ข้อมูลที่มีโครงสร้าง



---

## ⚖️ เนื้อหาจาก docs/ETHICS.md

### แนวทางจริยธรรมและกฎหมายในการ Web Scraping

1. **เคารพ robots.txt** — ตรวจสอบเสมอก่อน scrape ที่ `https://[domain]/robots.txt` และปฏิบัติตามกฎ
2. **ตรวจสอบ Terms of Service (ToS)** — หากไซต์ห้าม scraping ชัดเจน การ scrape ถือเป็นการละเมิดสัญญา อาจนำไปสู่การดำเนินคดี
3. **สุภาพ: Rate Limiting และ Delays** — หน่วงเวลา 2-5 วินาทีระหว่างการโหลดหน้า หลีกเลี่ยงการส่ง request พร้อมกันจำนวนมาก
4. **ระบุตัวตน (User-Agent)** — ใส่ User-Agent ที่ระบุตัวตนของ scraper ชัดเจน
5. **ไม่ปลอมตัวหรือซ่อนตัวในเชิงจริยธรรม** — ควรมีความโปร่งใส หลีกเลี่ยงเจตนาร้าย
6. **การใช้ข้อมูลและลิขสิทธิ์** — เนื้อหาที่ scrape มักมีลิขสิทธิ์ ไม่สามารถเผยแพร่ซ้ำโดยไม่ได้รับอนุญาต
7. **ข้อบังคับทางกฎหมายและความเสี่ยง** — รวมถึงการละเมิดสัญญา, trespass to chattels, การละเมิดลิขสิทธิ์, การละเมิดความเป็นส่วนตัวของข้อมูล

> **สรุป:** ควรปฏิบัติอย่างมีความรับผิดชอบ สุภาพ และถูกกฎหมายเสมอ หากไม่แน่ใจ ควรขออนุญาตจากเจ้าของเว็บไซต์โดยชัดเจน

---

## 📁 โครงสร้างโปรเจกต์

```text
agentic-web-scraper/
├── src/
│   ├── __init__.py          # ทำให้ 'src' เป็น Python package
│   ├── scraper_agent.py     # ตรรกะหลักของ agent (อ่าน config, ควบคุม selenium)
│   ├── config_parser.py     # จัดการการอ่านและตรวจสอบความถูกต้องของ configuration
│   ├── data_models.py       # Python class/dataclass สำหรับข้อมูลที่ scrape (เช่น Product)
│   ├── utils.py              # ฟังก์ชันช่วยเหลือ (เช่น waits, error handling)
│   └── driver_manager.py    # จัดการการตั้งค่า Selenium WebDriver (ใหม่)
├── configs/
│   └── example_site_config.json  # ไฟล์ config JSON สำหรับไซต์เฉพาะ
├── data/
│   └── scraped_products.json     # ข้อมูล output
├── main.py
├── .gitignore
└── README.md

```

---

## 🚀 คู่มือการ Setup โปรเจกต์ Agentic Web Scraper ใน VS Code

### ขั้นตอนที่ 1: ตรวจสอบและติดตั้งโปรแกรมที่จำเป็น

#### 1.1 ติดตั้ง Python

เปิด Terminal (cmd/PowerShell) แล้วตรวจสอบว่ามี Python หรือยัง:

```bash
python --version

```

*ถ้ายังไม่มี ให้ไปโหลดที่ python.org (แนะนำเวอร์ชัน 3.10+)* ⚠️ **สำคัญ:** ตอนติดตั้ง ให้ติ๊ก ✅ **"Add Python to PATH"** ด้วย

#### 1.2 ติดตั้ง VS Code

โหลดได้ที่ `code.visualstudio.com` (ถ้ามีอยู่แล้วข้ามได้)

#### 1.3 ติดตั้ง Extension ที่จำเป็นใน VS Code

เปิด VS Code → กด `Ctrl+Shift+X` (Extensions) แล้วค้นหาติดตั้ง:

* **Python** (โดย Microsoft)
* **Pylance** (มักติดมาพร้อม Python extension)

---

### ขั้นตอนที่ 2: สร้างโครงสร้างโปรเจกต์

#### 2.1 สร้างโฟลเดอร์โปรเจกต์

```bash
mkdir agentic-web-scraper
cd agentic-web-scraper

```

#### 2.2 เปิดโฟลเดอร์นี้ใน VS Code

```bash
code .

```

---

### ขั้นตอนที่ 3: สร้าง Virtual Environment (แนะนำอย่างยิ่ง)

การใช้ virtual environment ช่วยแยก dependency ของโปรเจกต์นี้ ไม่ปนกับโปรเจกต์อื่น

เปิด Terminal ใน VS Code (`Ctrl+~` หรือ `Terminal` → `New Terminal`):

```bash
python -m venv venv

```

**เปิดใช้งาน venv:**

* **Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1

```


*ถ้าเจอ error เรื่อง execution policy ให้รัน:*
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```


* **macOS/Linux:**
```bash
source venv/bin/activate

```



*เมื่อ activate สำเร็จ จะเห็น `(venv)` นำหน้าที่ prompt*

**ติดตั้ง Dependencies ที่จำเป็น:**

```bash
pip install selenium webdriver-manager

```

**เลือก Python Interpreter ให้ VS Code รู้จัก venv:**

1. กด `Ctrl+Shift+P`
2. พิมพ์ `Python: Select Interpreter`
3. เลือกตัวที่มีคำว่า `./venv/...`

---

### ขั้นตอนที่ 4: สร้างโครงสร้างไฟล์/โฟลเดอร์

สร้างโครงสร้างตามนี้ (คลิกขวาใน Explorer panel ของ VS Code → New Folder/New File) หรือใช้คำสั่งสร้างแบบรวดเร็วใน Terminal:

```text
agentic-web-scraper/
├── src/
│   ├── __init__.py          # ทำให้ 'src' เป็น Python package
│   ├── scraper_agent.py     # ตรรกะหลักของ agent (อ่าน config, ควบคุม selenium)
│   ├── config_parser.py     # จัดการการอ่านและตรวจสอบความถูกต้องของ configuration
│   ├── data_models.py       # Python class/dataclass สำหรับข้อมูลที่ scrape (เช่น Product)
│   ├── utils.py              # ฟังก์ชันช่วยเหลือ (เช่น waits, error handling)
│   └── driver_manager.py    # จัดการการตั้งค่า Selenium WebDriver (ใหม่)
├── configs/
│   └── example_site_config.json  # ไฟล์ config JSON สำหรับไซต์เฉพาะ
├── data/
│   └── scraped_products.json     # ข้อมูล output
├── main.py
├── .gitignore
└── README.md

```

* **Windows (Terminal):**
```cmd
mkdir src configs data docs
type nul > src\__init__.py
type nul > src\scraper_agent.py
type nul > src\config_parser.py
type nul > src\data_models.py
type nul > src\utils.py
type nul > src\driver_manager.py
type nul > configs\example_site_config.json
type nul > main.py
type nul > requirements.txt
type nul > .gitignore
type nul > README.md

```


*(macOS/Linux ให้ใช้ `touch` แทน `type nul >`)*

---

### ขั้นตอนที่ 5: สร้างไฟล์ requirements.txt และทดสอบ

เปิดไฟล์ `requirements.txt` แล้วเพิ่ม:

```text
selenium
webdriver-manager

```

จากนั้นติดตั้ง:

```bash
pip install -r requirements.txt

```

#### ✅ Checkpoint: ตรวจสอบว่าติดตั้งถูกต้อง

ลองสร้างไฟล์ทดสอบ `test_setup.py`:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://books.toscrape.com/")
print("Title:", driver.title)
driver.quit()

```

รันด้วย:

```bash
python test_setup.py

```

*ถ้าเห็น Chrome เปิดขึ้นมา, ไปที่เว็บ, แล้ว print ชื่อหน้าเว็บออกมาใน Terminal = Setup สำเร็จ! 🎉*

---

## 💻 โค้ดในแต่ละไฟล์ (สามารถก็อปไปวางได้เลย)

### 1. `src/data_models.py`

ไฟล์นี้ใช้สำหรับกำหนดโครงสร้างข้อมูลสินค้าที่จะจัดเก็บด้วย `@dataclass`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    price: str
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None

```

---

### 2. `src/driver_manager.py`

จัดการการเปิด-ปิด Selenium WebDriver รองรับทั้ง Chrome และ Firefox รวมถึงการตั้งค่า Headless Mode

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverManager:
    def __init__(self, browser_type: str = "chrome", headless: bool = True):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.driver = None

    def get_driver(self):
        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

        elif self.browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        self.driver.implicitly_wait(10)
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()

```

---

### 3. `src/config_parser.py`

ทำหน้าที่โหลดไฟล์คอนฟิก JSON และตรวจสอบว่ามี Key ที่จำเป็นครบถ้วนหรือไม่

```python
import json
import os

class ConfigParser:
    REQUIRED_KEYS = [
        "start_url",
        "max_pages",
        "delay_between_pages",
        "item_container_selector",
        "item_data_selectors"
    ]

    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self._validate_config(config)
        return config

    def _validate_config(self, config: dict):
        for key in self.REQUIRED_KEYS:
            if key not in config:
                raise KeyError(f"Missing required configuration key: '{key}'")

```

---

### 4. `src/utils.py`

ฟังก์ชันช่วยเหลือในการบันทึกข้อมูล และการรอ/คลิก Element อย่างปลอดภัย

```python
import json
import os
import time
from typing import List, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_data_to_json(data: List[Dict[str, Any]], filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def wait_for_element(driver, selector: str, timeout: int = 10, by: By = By.CSS_SELECTOR):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )

def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)
    element.click()

```

---

### 5. `src/scraper_agent.py`

ส่วนควบคุมหลักในการดึงข้อมูล และการเปลี่ยนหน้า (Pagination)

```python
import time
from dataclasses import asdict
from selenium.webdriver.common.by import By
from src.driver_manager import DriverManager
from src.data_models import Product
from src.utils import safe_click

class ScraperAgent:
    def __init__(self, config: dict, browser: str = "chrome", headless: bool = True):
        self.config = config
        self.driver_manager = DriverManager(browser_type=browser, headless=headless)
        self.driver = self.driver_manager.get_driver()

    def run(self) -> list:
        results = []
        try:
            self.driver.get(self.config["start_url"])
            current_page = 1

            while current_page <= self.config["max_pages"]:
                print(f"Scraping page {current_page}...")
                time.sleep(self.config["delay_between_pages"])

                items = self.driver.find_elements(By.CSS_SELECTOR, self.config["item_container_selector"])
                for item in items:
                    product_data = self._parse_item(item)
                    results.append(asdict(product_data))

                # Handle Pagination
                pagination_selector = self.config.get("pagination_selector")
                if pagination_selector and current_page < self.config["max_pages"]:
                    next_buttons = self.driver.find_elements(By.CSS_SELECTOR, pagination_selector)
                    if next_buttons:
                        safe_click(self.driver, next_buttons[0])
                        current_page += 1
                    else:
                        print("No next page button found. Stopping.")
                        break
                else:
                    break

        finally:
            self.driver_manager.close_driver()

        return results

    def _parse_item(self, item) -> Product:
        selectors = self.config["item_data_selectors"]
        
        def get_text(selector):
            if not selector: return None
            try:
                return item.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                return None

        def get_attr(selector, attr):
            if not selector: return None
            try:
                return item.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
            except:
                return None

        return Product(
            name=get_text(selectors.get("name")),
            price=get_text(selectors.get("price")),
            description=get_text(selectors.get("description")),
            url=get_attr(selectors.get("url"), "href"),
            image_url=get_attr(selectors.get("image_url"), "src")
        )

```

---

### 6. `configs/example_site_config.json`

ไฟล์คอนฟิกสำหรับทดสอบกับเว็บ `books.toscrape.com` (สร้างไฟล์นี้ไว้ในโฟลเดอร์ `configs/`)

```json
{
  "start_url": "https://books.toscrape.com/catalogue/category/books_1/index.html",
  "max_pages": 2,
  "delay_between_pages": 1,
  "item_container_selector": "article.product_pod",
  "pagination_selector": "li.next a",
  "item_data_selectors": {
    "name": "h3 a",
    "price": "p.price_color",
    "description": null,
    "url": "h3 a",
    "image_url": "div.image_container a img"
  }
}

```

---

### 7. `main.py`

ไฟล์หลักในการเรียกใช้งานระบบ

```python
import os
from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent
from src.utils import save_data_to_json

def main():
    config_path = os.path.join("configs", "example_site_config.json")
    output_path = os.path.join("data", "scraped_products.json")

    # 1. Load and parse config
    parser = ConfigParser(config_path)
    config = parser.load_config()

    # 2. Initialize and run scraper agent
    # ปรับ headless=False หากต้องการเปิดเบราว์เซอร์ดูการทำงานจริง
    agent = ScraperAgent(config=config, browser="chrome", headless=True)
    results = agent.run()

    # 3. Save results
    save_data_to_json(results, output_path)
    print(f"Successfully scraped {len(results)} items and saved to {output_path}")

if __name__ == "__main__":
    main()

```

---

## 🧪 การติดตั้ง Libraries และการทดสอบรันระบบ (Final Testing)

### 1. การติดตั้ง Libraries ที่จำเป็น

รันคำสั่งนี้ใน Terminal เพื่อตรวจสอบว่าติดตั้ง Package ครบถ้วนแล้วหรือไม่:

```bash
pip install selenium webdriver-manager

```

### 2. ขั้นตอนการทดสอบรันระบบ

ให้ทดสอบรันโปรแกรมผ่าน Terminal ด้วยคำสั่ง:

```bash
python main.py

```

### 3. ผลลัพธ์ที่ควรจะเกิดขึ้น

1. **Terminal แสดงข้อความการทำงาน เช่น:**
```text
Scraping page 1...
Scraping page 2...
Successfully scraped 40 items and saved to data/scraped_products.json

```


2. **มีไฟล์ `scraped_products.json` ถูกสร้างขึ้นภายในโฟลเดอร์ `data/**` ซึ่งบรรจุข้อมูลหนังสือ เช่น ชื่อ, ราคา, URL รูปภาพ ฯลฯ