# week6_labs.py
# Week 6: Functions & Modules
# โปรแกรมนี้รวม Lab 6.1 (Calculator) และ Lab 6.2 (Custom module + math/random) ไว้ในไฟล์เดียว
# เขียนแบบง่าย ๆ สำหรับคนเพิ่งเริ่มเรียนเขียนโปรแกรม

import math
import random


# ------------------------------------------------------------
# Lab 6.1: Simple Calculator Functions
# ------------------------------------------------------------

def add(a, b):
    """บวกเลขสองจำนวน แล้วคืนค่าผลบวก"""
    return a + b


def subtract(a, b):
    """ลบเลขสองจำนวน (a - b) แล้วคืนค่าผลลบ"""
    return a - b


def multiply(a, b):
    """คูณเลขสองจำนวน แล้วคืนค่าผลคูณ"""
    return a * b


def divide(a, b):
    """หารเลขสองจำนวน (a / b) แล้วคืนค่าผลหาร
    ถ้าตัวหาร (b) เป็น 0 จะคืนข้อความ error แทน เพื่อไม่ให้โปรแกรมพัง
    """
    if b == 0:
        return "Error: Division by zero"
    return a / b


def power(base, exponent=2):
    """ยกกำลัง base ด้วย exponent
    ถ้าไม่ระบุ exponent จะยกกำลังสอง (exponent=2) ให้เป็นค่าเริ่มต้น
    """
    return base ** exponent


def calculator_menu():
    """เมนูเครื่องคิดเลขแบบง่าย ๆ ใช้ while loop ให้ผู้ใช้เลือกคำนวณจนกว่าจะเลือกออก"""
    while True:
        print("\n----- เมนูเครื่องคิดเลข -----")
        print("1. บวก (Add)")
        print("2. ลบ (Subtract)")
        print("3. คูณ (Multiply)")
        print("4. หาร (Divide)")
        print("5. ยกกำลัง (Power)")
        print("6. ออกจากโปรแกรม")

        choice = input("เลือกเมนู (1-6): ")

        # ออกจากเมนูถ้าเลือก 6
        if choice == "6":
            print("ออกจากเครื่องคิดเลขแล้ว")
            break

        # เมนู 1-4 ต้องใช้ตัวเลข 2 จำนวน
        if choice in ("1", "2", "3", "4"):
            num1 = float(input("กรอกตัวเลขที่ 1: "))
            num2 = float(input("กรอกตัวเลขที่ 2: "))

            if choice == "1":
                result = add(num1, num2)
            elif choice == "2":
                result = subtract(num1, num2)
            elif choice == "3":
                result = multiply(num1, num2)
            elif choice == "4":
                result = divide(num1, num2)

            print("ผลลัพธ์ =", result)

        # เมนู 5 ยกกำลัง ให้เลือกได้ว่าจะใส่เลขยกกำลังเองหรือไม่
        elif choice == "5":
            base = float(input("กรอกฐาน (base): "))
            exp_input = input("กรอกเลขยกกำลัง (เว้นว่างไว้ = ยกกำลังสอง): ")

            if exp_input == "":
                result = power(base)
            else:
                result = power(base, float(exp_input))

            print("ผลลัพธ์ =", result)

        else:
            print("กรุณาเลือกเมนูให้ถูกต้อง (1-6)")


# ------------------------------------------------------------
# Lab 6.2: Custom Module and Standard Library Usage
# (ส่วนนี้ทำหน้าที่เหมือน my_utils.py แต่รวมไว้ในไฟล์เดียวกัน)
# ------------------------------------------------------------

def greet(name):
    """พิมพ์ข้อความทักทายชื่อที่รับเข้ามา"""
    print("Hello, " + name + "!")


def is_prime(number):
    """ตรวจสอบว่าตัวเลขที่รับเข้ามาเป็นจำนวนเฉพาะหรือไม่
    คืนค่า True ถ้าเป็นจำนวนเฉพาะ, False ถ้าไม่ใช่
    """
    if number < 2:
        return False

    # ลองหารด้วยเลขตั้งแต่ 2 ถึง number-1 ดูว่ามีตัวไหนหารลงตัวไหม
    for i in range(2, number):
        if number % i == 0:
            return False

    return True


def module_demo():
    """สาธิตการใช้งานฟังก์ชันของเราเอง (greet, is_prime) และโมดูลมาตรฐาน (math, random)"""
    print("\n----- ทดสอบฟังก์ชันของเราเอง -----")
    greet("Alice")

    for n in (7, 10):
        print(n, "เป็นจำนวนเฉพาะหรือไม่:", is_prime(n))

    print("\n----- ทดสอบโมดูลมาตรฐาน -----")
    number = 25
    sqrt_result = math.sqrt(number)
    print("รากที่สองของ", number, "คือ", sqrt_result)

    random_number = random.randint(1, 100)
    print("สุ่มตัวเลขระหว่าง 1-100 ได้:", random_number)


# ------------------------------------------------------------
# โปรแกรมหลัก
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=== Week 6: Functions & Modules ===")

    # Lab 6.2 เดโม่ก่อน (เพราะไม่ต้องพิมพ์ตอบโต้)
    module_demo()

    # Lab 6.1 เมนูเครื่องคิดเลข (ต้องพิมพ์โต้ตอบกับโปรแกรม)
    calculator_menu()
