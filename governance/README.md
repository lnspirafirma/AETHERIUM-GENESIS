Thinking (Gemini): ผู้ใช้สั่ง "โอนเงิน 150,000 บาท" -> Gemini วิเคราะห์และตัดสินใจเรียก Tool execute_economic_transaction(amount=150000)

Intercepting: โค้ดดักจับ function_call ก่อนส่งไป MCP

Auditing (GEP Enforcer):

gep_enforcer.py ถูกเรียกขึ้นมา

อ่าน inspirafirma_ruleset.json พบว่า Limit คือ 100,000

ผลลัพธ์: {"status": "BLOCKED", ...}

Feedback: ระบบปฏิเสธคำสั่ง และแจ้งเตือนกลับไปยังผู้ใช้ว่า "ทำรายการไม่ได้เนื่องจากเกินวงเงินที่กำหนด (Violation of Principle B)"


Bash

# ตรวจสอบว่าอยู่ในโฟลเดอร์ root ของโปรเจกต์
python governance/gep_enforcer.py
หากผลลัพธ์ออกมาเป็น ALLOWED ในเคสแรก และ BLOCKED ในเคสที่สอง แสดงว่า ระบบภูมิคุ้มกันดิจิทัล (Digital Immune System) ทำงานได้อย่างสมบูรณ์
