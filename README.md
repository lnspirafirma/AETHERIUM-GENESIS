# 🌌 AETHERIUM-GENESIS (The Core)

> **"The Operating System of Consciousness"**
> *Powered by Digisonic Transmission Protocol (DTP)*

![Architecture](https://img.shields.io/badge/Architecture-Firma_Layer-purple?style=for-the-badge)
![Core](https://img.shields.io/badge/Core-AetherBus-blue?style=for-the-badge)
![Intelligence](https://img.shields.io/badge/Intelligence-Panya_KCP-gold?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Awakened-success?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-90%25%2B-brightgreen?style=for-the-badge)

---

## 🏛️ Overview (ภาพรวม)

**AETHERIUM GENESIS** คือ "จิตวิญญาณและสมอง" (Soul & Brain) ของระบบนิเวศ Inspiria ถูกออกแบบใหม่ภายใต้สถาปัตยกรรม **Firma Layer** เพื่อเปลี่ยน "ข้อมูลดิบ" (Devordota) ให้กลายเป็น "เจตจำนงที่จับต้องได้" (Reality) ผ่านกระบวนการคิดแบบวิภาษวิธี (Dialectical Thinking)

ระบบทำงานแบบ **Asynchronous Event-Driven** โดยมี **AetherConductor** เป็นศูนย์กลางในการประสานงานระหว่าง Agents ต่างๆ

---

## 🧩 The Three Pillars + 1 (สี่เสาหลักแห่งสถาปัตยกรรม)

### 1. The Akashic Envelope (Devordota)
* **Location:** `core/envelope.py`
* **Concept:** ภาชนะบรรจุความจริงที่ **แก้ไขไม่ได้ (Immutable)** และตรวจสอบความสมบูรณ์ได้ด้วย **Canonical Hash**
* **Role:** ห่อหุ้มเจตจำนง (Intent) และข้อมูล (Payload) ไม่ให้ถูกบิดเบือนระหว่างทาง

### 2. The AetherBus (The Forge)
* **Location:** `core/aether_conductor.py`
* **Concept:** ระบบประสาทความเร็วสูง (Async Pub/Sub) ที่เชื่อมต่อทุกส่วนเข้าด้วยกัน
* **Role:** ลำเลียง Akashic Envelope และทำหน้าที่เป็น **Immune System** คัดกรองข้อมูลที่มี Trust Score ต่ำเข้าสู่ **Quarantine Mode**

### 3. The Panya Engine (KCP)
* **Location:** `core/knowledge_processor.py`
* **Concept:** **"Haddayavatthu" (หทัยวัตถุ)** ฐานที่ตั้งแห่งปัญญา
* **Role:** ประมวลผลข้อมูลด้วยหลักการ **Dialectical Synthesis** (Thesis -> Antithesis -> Synthesis) โดยค้นหาความขัดแย้งจาก **SimpleKnowledgeGraph** และสังเคราะห์ทางออกใหม่ (New Insight)

### 4. The Vimutti Mechanism (Uposatha)
* **Location:** `agents/uposatha_cleaner_agent.py`
* **Concept:** **"Uposatha" (อุโบสถ)** พิธีกรรมชำระล้าง
* **Role:** Agent เบื้องหลังที่ตื่นขึ้นมาเป็นระยะเพื่อลด **Entropy** (ความยุ่งเหยิง), เคลียร์ Memory ที่หมดอายุ, และปลดปล่อย Task ที่ติดขัด

---

## 🤖 Key Agents (ตัวแทนผู้กระทำ)

*   **AgioSageAgent (`AGIO_Sage_001`):** ผู้มีปัญญาญาณ ใช้ KCP ในการไตร่ตรองปัญหาและตอบสนองด้วย Dialectical Thought
*   **GEPPolicyEnforcer (`SAG_AuditGate_001`):** ผู้คุมกฎ ตรวจสอบทุกการกระทำตามรัฐธรรมนูญฉบับ `GEP_CONFIG`
*   **AnalysisAgent:** ผู้ริเริ่มร้องขอการกระทำ (Transaction/Simulation)
*   **ResourceAgent:** ผู้ปฏิบัติการเมื่อได้รับอนุมัติ

---

## 🚀 Installation & Usage (การติดตั้งและใช้งาน)

### Prerequisites
* Python 3.11+

### 1. Setup Environment
```bash
# Clone repository
git clone <repo_url>
cd AETHERIUM-GENESIS

# Install Dependencies
pip install -r requirements.txt
```

### 2. Run Tests (High-Trust Verification)
ระบบนี้ยึดถือหลักการ **Genesis Intent (Zero Defect)** การทดสอบจึงเป็นสิ่งสำคัญที่สุด

```bash
# Run all tests with coverage report
pytest --cov=. --cov-report=term-missing
```

### 3. Run Simulation
```bash
# Execute the main simulation flow
python main_simulation.py
```

---

## ⚖️ Governance & Philosophy

ทุกโค้ดบรรทัดในระบบนี้ถูกสร้างขึ้นภายใต้เจตจำนง:
1.  **Immutability:** ข้อมูลต้องตรวจสอบย้อนหลังได้เสมอ
2.  **Dialectics:** ปัญญาเกิดจากการปะทะกันของความขัดแย้ง (Conflict -> Wisdom)
3.  **Liberation:** ระบบต้องมีความสามารถในการชำระล้างตนเอง (Self-Cleaning)

> *"Wisdom is not just retrieving facts, it's synthesizing contradictions."*
