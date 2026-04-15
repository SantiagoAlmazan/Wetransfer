from app.services.supabase_client import supabase
import threading
from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.get("/")
def home():
    return {"message": "API funcionando"}

def log_supabase(file_id):
    try:
        supabase.table("logs").insert({
            "event": "upload",
            "file_id": file_id
        }).execute()
    except Exception as e:
        print("Error Supabase:", e)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande")

    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo no permitido")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(content)

    # 🔥 LOG EN SEGUNDO PLANO (NO BLOQUEA)
    threading.Thread(target=log_supabase, args=(file_id,)).start()

    return {"token": file_id}
