try:
    # Task 2: รับอายุจากผู้ใช้และแปลงเป็นจำนวนเต็ม (Integer)
    age = int(input("Enter your age: "))
    
    # Task 4 (Challenge): ถามคำถามรอง "ชอบหนังแอ็กชันไหม?"
    like_action = input("Do you like action movies? (yes/no): ").strip().lower()

    print("--- Movie Recommendation ---")

    # Task 3 & 4: ตรวจสอบเงื่อนไขตามตรรกะที่กำหนด
    
    # เงื่อนไขที่ 1: อายุน้อยกว่า 5 ปี
    if age < 5:
        print("You're too young for movies! Enjoy cartoons.")
        
    # เงื่อนไขที่ 2: อายุ 5 ถึง 12 ปี (ใช้ <= เพื่อรวมช่วงอายุด้วย)
    elif age >= 5 and age <= 12:
        print("Recommend: G-rated or PG-rated movies.")
        
    # เงื่อนไขที่ 3: อายุ 13 ถึง 17 ปี
    elif age >= 13 and age <= 17:
        print("Recommend: PG-13 or R-rated (with parental guidance).")
        
    # เงื่อนไขที่ 4: อายุ 18 ปีขึ้นไป
    else:
        print("Recommend: Any movie rating.")
        
        # 🚨 Challenge: ถ้าอายุ 18 ขึ้นไป และชอบหนังแอ็กชัน (like_action เป็น 'yes')
        if like_action == "yes":
            print("You might enjoy the latest action blockbuster!")

except ValueError:
    print("Error: Please enter a valid integer for age.")