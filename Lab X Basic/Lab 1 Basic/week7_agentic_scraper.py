# week7_agentic_scraper.py
# Week 7 (Advanced): Agentic Web Scraper ด้วย Selenium + Config File
# แนวคิด: เขียน scraper ที่ "อ่านกฎ" จากไฟล์ config (.json) แทนการฝังค่าตายตัวในโค้ด
#          ทำให้เปลี่ยนเว็บเป้าหมาย/ตัวเลือกข้อมูลได้ โดยไม่ต้องแก้โค้ด (เหมือน agent ทำตามแผน)
#
# เขียนแบบง่าย ๆ สำหรับคนเพิ่งเริ่มเรียนเขียนโปรแกรม (รวมทุกอย่างไว้ไฟล์เดียว)
# ก่อนรันต้องติดตั้งไลบรารีก่อน:
#   pip install selenium webdriver-manager

import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

CONFIG_PATH = "week7_agentic_config.json"
OUTPUT_PATH = "scraped_products.json"


def load_config(path):
    """อ่านไฟล์ config (.json) แล้วคืนค่าเป็น dictionary
    นี่คือ "แผนงาน" ที่บอก agent ว่าต้อง scrape เว็บไหน และดึงข้อมูลตรงไหนบ้าง
    """
    if not os.path.exists(path):
        raise FileNotFoundError("ไม่พบไฟล์ config: " + path)

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config


def create_browser(headless=True):
    """สร้างและคืนค่า Selenium WebDriver (เบราว์เซอร์ Chrome ที่ควบคุมด้วยโค้ด)"""
    options = webdriver.ChromeOptions()

    if headless:
        # headless = รันเบราว์เซอร์แบบไม่เปิดหน้าต่างให้เห็น (เร็วกว่า)
        options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.implicitly_wait(10)  # รอ element สูงสุด 10 วินาทีก่อนจะถือว่าหาไม่เจอ

    return browser


def scrape_one_item(item_element, data_selectors):
    """ดึงข้อมูลของสินค้า/บทความ 1 ชิ้น ตาม selector ที่กำหนดไว้ใน config
    คืนค่าเป็น dictionary เช่น {"name": ..., "price": ..., "url": ...}
    """
    product = {}

    for field_name, selector in data_selectors.items():
        if not selector:
            product[field_name] = None
            continue

        try:
            element = item_element.find_element(By.CSS_SELECTOR, selector)

            # ฟิลด์ที่ชื่อลงท้ายด้วย _url ให้ดึงจาก attribute (href หรือ src) แทนข้อความ
            if field_name == "url":
                product[field_name] = element.get_attribute("href")
            elif field_name == "image_url":
                product[field_name] = element.get_attribute("src")
            else:
                product[field_name] = element.text.strip()
        except Exception:
            # ถ้าหา element ไม่เจอ ก็ใส่ None ไว้แทน ไม่ให้โปรแกรมพัง
            product[field_name] = None

    return product


def run_agent(config):
    """ฟังก์ชันหลักของ agent: อ่าน config แล้วเริ่ม scrape ตามแผน
    ทำงานเป็นลูป: ดึงข้อมูลหน้านี้ -> หาปุ่มหน้าถัดไป -> คลิก -> ทำซ้ำ จนครบ max_pages
    """
    browser = create_browser(headless=True)
    all_products = []

    try:
        browser.get(config["start_url"])
        current_page = 1

        while current_page <= config["max_pages"]:
            print("กำลัง scrape หน้าที่", current_page, "...")
            time.sleep(config["delay_between_pages"])  # หน่วงเวลาให้เว็บโหลดและไม่โหลดถี่เกินไป

            items = browser.find_elements(By.CSS_SELECTOR, config["item_container_selector"])
            for item in items:
                product = scrape_one_item(item, config["item_data_selectors"])
                all_products.append(product)

            # หาปุ่ม/ลิงก์ไปหน้าถัดไป ถ้ายังไม่ถึงหน้าสุดท้ายที่ตั้งไว้
            if current_page >= config["max_pages"]:
                break

            next_buttons = browser.find_elements(By.CSS_SELECTOR, config["pagination_selector"])
            if not next_buttons:
                print("ไม่พบปุ่มหน้าถัดไป หยุดการทำงาน")
                break

            browser.execute_script("arguments[0].scrollIntoView(true);", next_buttons[0])
            time.sleep(0.5)
            next_buttons[0].click()
            current_page += 1

    finally:
        browser.quit()

    return all_products


def save_to_json(data, path):
    """บันทึกข้อมูลที่ scrape ได้ลงไฟล์ .json"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    config = load_config(CONFIG_PATH)
    products = run_agent(config)

    save_to_json(products, OUTPUT_PATH)
    print("scrape ข้อมูลสำเร็จ", len(products), "รายการ, บันทึกลงไฟล์:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
