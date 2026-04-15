from app.services.supabase_client import supabase
from app.database.connection import SessionLocal
from datetime import datetime, timedelta
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

    # 🔐 Validaciones
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande")

    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo no permitido")

    # 📁 Guardar archivo
    file_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(content)

    # 🗄️ Guardar en PostgreSQL
    db = SessionLocal()

    try:
        db.execute("""
            INSERT INTO files (
                id, filename, stored_name, file_size, mime_type, token, expires_at, status
            ) VALUES (
                :id, :filename, :stored_name, :file_size, :mime_type, :token, :expires_at, :status
            )
        """, {
            "id": file_id,
            "filename": file.filename,
            "stored_name": file_id,
            "file_size": len(content),
            "mime_type": file.content_type,
            "token": token,
            "expires_at": datetime.now() + timedelta(hours=1),
            "status": "active"
        })

        db.commit()

    except Exception as e:
        db.rollback()
        print("Error DB:", e)
        raise HTTPException(status_code=500, detail="Error guardando en base de datos")

    finally:
        db.close()

    return {"token": token}
