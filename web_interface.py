# web_interface.py
import asyncio
import json
from datetime import datetime
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import Core Components ของคุณ
from core.aether_conductor import conductor
from core.envelope import Envelope, AetherIntent
from core.agio_identity import MindLogic

app = FastAPI(title="Aetherium Resonance Console")

# จำลอง State ของระบบ (ในระบบจริงจะดึงจาก AkashicLedger)
system_state = {
    "sati_level": 0.85,
    "current_mood": "Equanimity (อุเบกขา)",
    "active_agents": ["AgioSage", "GEP_Enforcer", "UposathaCleaner"],
    "last_thought": "Waiting for architect's intent..."
}

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# --- Aether Integration ---
# ฟังเสียงจาก Conductor แล้วส่งเข้า WebSocket
async def aether_listener(envelope: Envelope):
    """แปลง Envelope เป็นสัญญาณส่งไปยังหน้าเว็บ"""
    log_entry = {
        "type": "LOG",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "sender": envelope.sender_id,
        "intent": envelope.intent.name,
        "payload": str(envelope.payload)[:100] + "..." # ตัดให้สั้น
    }
    await manager.broadcast(log_entry)

# Hook เข้ากับ Conductor
@app.on_event("startup")
async def startup_event():
    # Subscribe หัวข้อต่างๆ จาก Core
    await conductor.subscribe("aether.tasks.pending", aether_listener)
    await conductor.subscribe("aether.tasks.approved", aether_listener)
    await conductor.subscribe("cognition.thought_stream", aether_listener)
    print("✅ ARC Interface connected to AetherBus")

# --- Endpoints ---

@app.get("/")
async def get_console():
    # โหลดไฟล์ HTML (ดูโค้ดส่วนที่ 2)
    with open("templates/console.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/api/inject_intent")
async def inject_intent(request: Request):
    """ส่งคำสั่ง (Intent) เข้าสู่ระบบ"""
    data = await request.json()
    intent_text = data.get("intent")
    
    # สร้าง Envelope และส่งเข้า Bus (ตามมาตรฐาน protocol ของคุณ)
    env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="ARC_Console",
        payload={"tool_call": "manual_override", "instruction": intent_text, "_security_context": "Architect_Override"}
    )
    
    # Fire and forget
    asyncio.create_task(conductor.publish("aether.tasks.pending", env))
    
    return {"status": "Intent Injected", "id": env.msg_id}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # ส่ง Initial State
        await websocket.send_json({"type": "STATE", "data": system_state})
        while True:
            # Keep alive
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)