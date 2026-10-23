# src/task.py

class Task:
    """
    คลาสสำหรับจำลองข้อมูลงานแต่ละรายการ (Single Task)
    
    Attributes:
        id (int): รหัสประจำงานที่ไม่ซ้ำกัน
        description (str): รายละเอียดข้อความของงาน
        completed (bool): สถานะการทำงาน (True = ทำเสร็จแล้ว, False = ยังไม่เสร็จ)
    """

    def __init__(self, id: int, description: str, completed: bool = False):
        """
        Constructor สำหรับสร้าง Instance ของ Task
        
        Args:
            id (int): รหัสของงาน
            description (str): คำอธิบายงาน
            completed (bool, optional): สถานะงาน เริ่มต้นเป็น False
        """
        # TODO 1.1: กำหนดค่าให้กับ instance attributes (อย่าลืมใช้คำว่า self)
        # 1. กำหนด self.id จากค่า id ที่รับเข้ามา
        # 2. กำหนด self.description จากค่า description ที่รับเข้ามา
        # 3. กำหนด self.completed จากค่า completed ที่รับเข้ามา
        raise NotImplementedError("TODO 1.1: กำหนด instance attributes ใน __init__")

    def mark_complete(self):
        """
        Method สำหรับเปลี่ยนสถานะของงานนี้ให้เป็นเสร็จสมบูรณ์ (completed = True)
        """
        # TODO 1.2: เปลี่ยนค่าของ self.completed ให้เป็น True
        raise NotImplementedError("TODO 1.2: ทำฟังก์ชัน mark_complete ให้เปลี่ยนสถานะ completed เป็น True")

    def to_dict(self) -> dict:
        """
        แปลงข้อมูลจาก Task Object ให้อยู่ในรูป Dictionary
        เพื่อความสะดวกในการบันทึกลงไฟล์ JSON (Serialization)
        
        Returns:
            dict: เช่น {"id": 1, "description": "Buy milk", "completed": False}
        """
        # TODO 1.3: return dictionary ที่มี key 'id', 'description', 'completed'
        raise NotImplementedError("TODO 1.3: แปลง Task object เป็น dictionary")

    def __str__(self) -> str:
        """
        Dunder method สำหรับส่งคืนข้อความที่อ่านง่ายเมื่อใช้ print(task) หรือ str(task)
        
        Returns:
            str: รูปแบบ "ID: <id> | Description: <desc> | Status: Completed/Pending"
        """
        # TODO 1.4: คืนค่า string representation
        # คำแนะนำ: ตรวจสอบสถานะถ้า self.completed เป็น True ให้ใช้ "Completed" ถ้าไม่ใช่ให้ใช้ "Pending"
        raise NotImplementedError("TODO 1.4: จัดรูปแบบ string representation ใน __str__")

    def __repr__(self) -> str:
        """
        Dunder method สำหรับส่งคืน string เชิงเทคนิค สำหรับการ Debugging
        
        Returns:
            str: รูปแบบ "Task(id=<id>, description='<desc>', completed=<completed>)"
        """
        # TODO 1.5: คืนค่า string ทางเทคนิค
        raise NotImplementedError("TODO 1.5: คืนค่า representation สำหรับ debug ใน __repr__")
