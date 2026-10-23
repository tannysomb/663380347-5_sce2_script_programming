# week7_basic_scraper.py
# Week 7 (Basic): Introduction to Web Scraping
# ใช้ requests ดาวน์โหลดหน้าเว็บ และใช้ BeautifulSoup4 ดึงข้อมูลจาก HTML
# เขียนแบบง่าย ๆ สำหรับคนเพิ่งเริ่มเรียนเขียนโปรแกรม

import requests
from bs4 import BeautifulSoup

# เว็บไซต์ที่จะ scrape (เว็บเพื่อการศึกษา เปิดให้เข้าถึงได้ ไม่มีปัญหาด้านจริยธรรม)
TARGET_URL = "https://automatetheboringstuff.com/3e/"


def get_html_content(url):
    """ดาวน์โหลด HTML จาก url ที่กำหนด และคืนค่าเป็นข้อความ (string)
    ถ้าดาวน์โหลดไม่สำเร็จ จะคืนค่า None แทนการทำให้โปรแกรมพัง
    """
    print("กำลังดาวน์โหลดเนื้อหาจาก:", url)

    # ใส่ User-Agent ปลอมเป็นเบราว์เซอร์จริง เพราะบางเว็บบล็อก request ที่ไม่มี header นี้
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # ถ้า status ไม่ใช่ 200 จะโยน error ออกมา
        print("ดาวน์โหลดสำเร็จ (status code:", response.status_code, ")")
        return response.text
    except requests.exceptions.RequestException as e:
        print("ดาวน์โหลดไม่สำเร็จ:", e)
        return None


def scrape_book_and_chapters(html_content):
    """รับ HTML เป็นข้อความ แล้วดึงชื่อหนังสือและรายชื่อบทออกมา
    คืนค่าเป็น dictionary ที่มี book_title และ chapter_titles
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # --- หาชื่อหนังสือ ---
    # โครงสร้างหน้านี้: <article> -> <header> -> <h1>
    book_title = "ไม่พบชื่อหนังสือ"
    article_tag = soup.find("article")
    if article_tag:
        header_tag = article_tag.find("header")
        if header_tag:
            h1_tag = header_tag.find("h1")
            if h1_tag:
                book_title = h1_tag.get_text(strip=True)

    # --- หารายชื่อบท ---
    # โครงสร้างหน้านี้: <div class="content-body"> -> <ul> -> <li> -> <a>
    chapter_titles = []
    content_body = soup.find("div", class_="content-body")
    if content_body:
        chapter_links = content_body.select("ul li a")
        for link in chapter_links:
            title = link.get_text(strip=True)
            if title:
                chapter_titles.append(title)

    return {
        "book_title": book_title,
        "chapter_titles": chapter_titles,
    }


def main():
    html_content = get_html_content(TARGET_URL)

    if html_content is None:
        print("ไม่สามารถดาวน์โหลดหน้าเว็บได้ โปรแกรมจบการทำงาน")
        return

    result = scrape_book_and_chapters(html_content)

    print("\n--- ข้อมูลที่ Scrape ได้ ---")
    print("ชื่อหนังสือ:", result["book_title"])

    print("\nชื่อบทต่าง ๆ:")
    if result["chapter_titles"]:
        for i, title in enumerate(result["chapter_titles"]):
            print(str(i + 1) + ".", title)
    else:
        print("ไม่พบชื่อบทใด ๆ")

    print("--------------------")


if __name__ == "__main__":
    main()
