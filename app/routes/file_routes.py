
from app.services.supabase_client import supabase
from app.database.connection import SessionLocal
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
from datetime import datetime
import threading
from sqlalchemy import text
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

    # Validaciones
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande")

    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo no permitido")

    # Guardar archivo
    file_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(content)

    db = SessionLocal()

    try:
        db.execute(text("""
            INSERT INTO files (
                id, filename, stored_name, file_size, mime_type, token, expires_at, status
            ) VALUES (
                :id, :filename, :stored_name, :file_size, :mime_type, :token, :expires_at, :status
            )
        """), {
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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

    return {"token": token}


@router.get("/download/{token}")
def download_file(token: str):
    db = SessionLocal()

    try:
        result = db.execute(text("""
            SELECT stored_name, filename, expires_at, status
            FROM files
            WHERE token = :token
        """), {"token": token}).fetchone()

    except Exception as e:
        print("Error DB:", e)
        raise HTTPException(status_code=500, detail="Error en base de datos")

    finally:
        db.close()

    #No existe
    if not result:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    stored_name, filename, expires_at, status = result

    # Estado inválido
    if status != "active":
        raise HTTPException(status_code=400, detail="Archivo no disponible")

    # Expirado
    if datetime.now() > expires_at:
        raise HTTPException(status_code=400, detail="Archivo expirado")

    file_path = os.path.join(UPLOAD_DIR, stored_name)

    # No existe físicamente
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado en servidor")

    # ✅ Descargar archivo
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )