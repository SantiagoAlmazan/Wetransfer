from fastapi import APIRouter, UploadFile, File
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.get("/")
def home():
    return {"message": "API funcionando"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Generar nombre único
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id)

    # Leer archivo
    content = await file.read()

    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(content)

    return {"token": file_id}