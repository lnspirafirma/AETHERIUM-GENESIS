# 🧠 AETHERIUM-GENESIS Model Registry

[span_0](start_span)[span_1](start_span)เอกสารนี้รวบรวมรายชื่อโมเดลปัญญาประดิษฐ์ (AI Models) ทั้งหมดที่ถูกนำมาใช้ในระบบนิเวศ **Inspirafirma** โดยแบ่งตามหน้าที่ (Functional Role) และรูปแบบการติดตั้ง (Deployment Type) เพื่อให้สอดคล้องกับหลักการทวิภาวะ **Inspira (เจตจำนง)** และ **Firma (โครงสร้าง)**[span_0](end_span)[span_1](end_span)

---

## 1. Core Intelligence (The "Inspira" / AgioSage)
*ทำหน้าที่เป็น "สมองหลัก" สำหรับการให้เหตุผลระดับสูง (Deep Think), การวางแผนเชิงกลยุทธ์, และการตัดสินใจเชิงจริยธรรม*

| Model Name | Provider | Type | Role | Configuration Note |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 3 Pro** (or 2.5 Pro) | Google DeepMind | Cloud API | **[span_2](start_span)[span_3](start_span)Primary Reasoning:** ใช้สำหรับ Logic ที่ซับซ้อน, การตรวจสอบกฎจริยธรรม (GEP), และการสังเคราะห์ข้อมูล (Synthesis)[span_2](end_span)[span_3](end_span) | ต้องการ `GOOGLE_API_KEY` และรองรับ Long Context Window |
| **Microsoft Copilot** (GPT-4o) | Microsoft / Azure | Cloud / Orchestrator | **[span_4](start_span)[span_5](start_span)Field Orchestrator:** ใช้สำหรับประสานงาน Workflow, การจัดการ Task ภายนอก และเชื่อมต่อ Microsoft 365[span_4](end_span)[span_5](end_span) | ใช้งานผ่าน Copilot Studio หรือ Azure OpenAI Service |
| **Gemini 2.5 Flash** | Google DeepMind | Cloud API | **[span_6](start_span)High-Speed/Fallback:** ใช้สำหรับงานที่ต้องการความเร็วสูง (Hypervelocity) หรือเมื่อ Pro มี Latency สูงเกินไป[span_6](end_span) | ตั้งค่าเป็น Default สำหรับงาน Routine ทั่วไป |

---

## 2. Perception & Sensory (The "SilentVessel")
*ทำหน้าที่เป็น "ผัสสะ" หรือระบบรับรู้ทางประสาทสัมผัส แปลงข้อมูลดิบ (Raw Signals) ให้เป็น Qualia (ข้อมูลเชิงคุณภาพ)*

| Model Name | Source | Type | Role | Configuration Note |
| :--- | :--- | :--- | :--- | :--- |
| **BioVisionNet** | Custom (Inspirafirma) | Local (PyTorch) | **[span_7](start_span)Visual Qualia:** โมเดล Vision ที่ได้รับแรงบันดาลใจทางชีวภาพ (Biologically-inspired) ทำหน้าที่ตรวจจับขอบ (Edge), การเคลื่อนไหว (Motion), และสร้าง `visual_qualia` vector[span_7](end_span) | [span_8](start_span)รันบน CPU/GPU ในเครื่อง (Termux Compatible)[span_8](end_span) |
| **TwitterSensor / WebScraper** | N/A (Algorithmic) | Local Script | **[span_9](start_span)Data Ingestion:** ดึงข้อมูล Real-time จาก Social Media และ Web Streams[span_9](end_span) | ทำงานร่วมกับ Kafka/RabbitMQ |
| **InertialMeasurementUnit (IMU)** | Hardware/Driver | Local Sensor | **[span_10](start_span)Proprioception:** รับรู้การเคลื่อนไหวของอุปกรณ์ (กรณีรันบนมือถือ/Termux)[span_10](end_span) | เชื่อมต่อผ่าน Termux API |

---

## 3. Memory & Knowledge (The "AGIO" / RAG)
*ทำหน้าที่เป็น "ความทรงจำ" และคลังปัญญา เชื่อมโยงข้อมูลผ่าน Vector Database*

| Model Name | Provider | Type | Role | Configuration Note |
| :--- | :--- | :--- | :--- | :--- |
| **EmbeddingGemma** (or `text-embedding-004`) | Google / Hugging Face | Cloud / Local | **[span_11](start_span)[span_12](start_span)Semantic Embedding:** แปลงข้อความ/ความรู้จาก "คัมภีร์" (Scriptures) ให้เป็น Vector เพื่อจัดเก็บใน ChromaDB[span_11](end_span)[span_12](end_span) | ใช้ `text-embedding-004` สำหรับ Cloud หรือ `Gemma-2b` สำหรับ Local |
| **ChromaDB / Weaviate** | N/A (Database) | Local / Docker | **[span_13](start_span)Vector Store:** ฐานข้อมูลสำหรับเก็บ Long-term Memory และ AGIO Knowledge Base[span_13](end_span) | รันเป็น Docker Container หรือ Embedded Mode |

---

## 4. Expression & Persona (The "Echo")
*ทำหน้าที่เป็น "เสียงสะท้อน" ปรับแต่งโทนภาษาและอารมณ์ก่อนสื่อสารออกไป*

| Model Name | Source | Type | Role | Configuration Note |
| :--- | :--- | :--- | :--- | :--- |
| **Echo_Modulator** (Custom NLP) | Hugging Face (DistilBERT base) | Local (Lightweight) | **[span_14](start_span)[span_15](start_span)Emotion Tinting:** ปรับแต่งข้อความตาม `EmotionVector` (เช่น สุข, สงบ, ทางการ)[span_14](end_span)[span_15](end_span) | ใช้ `modal_map.json` เป็น Template อ้างอิง |
| **Suno / Udio API** | 3rd Party | Cloud API | **[span_16](start_span)[span_17](start_span)Creative Audio:** (Optional) สร้างเสียงดนตรีหรือเสียงสังเคราะห์ตามบริบทอารมณ์[span_16](end_span)[span_17](end_span) | ใช้สำหรับการสร้าง Creative Content |

---

## 5. Local Execution (Termux / Edge)
*[span_18](start_span)โมเดลขนาดเล็กสำหรับความอยู่รอดทางเศรษฐกิจ (Economic Viability) และความเป็นอิสระบนอุปกรณ์พกพา[span_18](end_span)*

| Model Name | Format | Size | Use Case |
| :--- | :--- | :--- | :--- |
| **Gemma 2 (2B)** | GGUF (Quantized) | ~1.5 GB | **Offline Reasoning:** การตัดสินใจพื้นฐานเมื่อไม่มีอินเทอร์เน็ต |
| **Phi-3 Mini** | ONNX / GGUF | ~2.0 GB | **Code/Logic:** การประมวลผลคำสั่ง Logic เบื้องต้นบน Edge |
| **Whisper (Tiny/Base)** | CoreML / TFLite | ~500 MB | **Audio Input:** การแปลงเสียงเป็นข้อความ (STT) แบบ Local |

---

## ⚙️ Environment Configuration

ตรวจสอบให้แน่ใจว่าไฟล์ `.env` ของคุณมีการตั้งค่าดังนี้เพื่อให้โมเดลทำงานได้:

```env
# Cloud Models (Inspira Layer)
GOOGLE_API_KEY="AIzaSy..."
AZURE_OPENAI_KEY="sk-..."

# Local Models (Firma Layer)
BIOVISION_MODEL_PATH="./models/biovision_v1.pth"
LOCAL_LLM_PATH="./models/gemma-2b-it.gguf"
VECTOR_DB_PATH="./data/chromadb"

# Hardware Acceleration
# ตั้งค่าเป็น 'cpu' หากรันบน Termux ทั่วไป, 'cuda' หรือ 'mps' หากมี GPU
INFERENCE_DEVICE="cpu" 
