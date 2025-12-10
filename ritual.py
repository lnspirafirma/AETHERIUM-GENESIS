import hashlib
import time
import uuid
from datetime import datetime
import sys

def seal_intent():
    """
    สร้างข้อความ Commit ที่มี Digital Signature
    """
    print("\n\n#################################################")
    print("### MOBILE COMMIT RITUAL: SIGNATURE GENERATOR ###")
    print("#################################################")
    print("Architect, please state your Intent (เจตนา):")
    
    try:
        # ใช้ sys.stdin.readline() เพื่อรองรับการทำงานในบางสภาพแวดล้อมมือถือ
        intent = input(">>> ").strip()
    except EOFError:
        intent = ""

    if not intent:
        print("\n❌ Intent cannot be empty. Aborting.")
        return

    # สร้างรหัสลับ (Sealing)
    timestamp = datetime.now().isoformat()
    salt = str(uuid.uuid4())[:8]
    secret = f"MOBILE-KEY:{intent}:{timestamp}:{salt}"
    sig = hashlib.sha256(secret.encode()).hexdigest()[:12]

    print("\n✨ --- RITUAL COMPLETE (COPY BELOW) ---")
    print("------------------------------------------------")
    print(f"FEAT: {intent}")
    print(f"")
    print(f"[AETHERIUM-SEAL]")
    print(f"Device: Mobile-Terminal")
    print(f"Time: {timestamp}")
    print(f"Signature: {sig}")
    print("------------------------------------------------")

if __name__ == "__main__":
    seal_intent()

