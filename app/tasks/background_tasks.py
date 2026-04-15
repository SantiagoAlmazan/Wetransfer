import os
import asyncio
from datetime import datetime
from sqlalchemy import text

from app.database.connection import SessionLocal

UPLOAD_DIR = "uploads"

async def cleanup_expired_files():
    while True:
        db = SessionLocal()

        try:
            # 1. Buscar archivos expirados
            result = db.execute(text("""
                SELECT stored_name
                FROM files
                WHERE expires_at < NOW()
                AND status = 'active'
            """)).fetchall()

            # 2. Borrar archivos físicos
            for row in result:
                file_path = os.path.join(UPLOAD_DIR, row[0])

                if os.path.exists(file_path):
                    os.remove(file_path)

            # 3. Marcar como expirados en BD
            db.execute(text("""
                UPDATE files
                SET status = 'expired'
                WHERE expires_at < NOW()
                AND status = 'active'
            """))

            db.commit()

            print(f"[CLEANUP] OK {datetime.now()} | eliminados: {len(result)}")

        except Exception as e:
            print("[CLEANUP ERROR]", e)

        finally:
            db.close()

        # espera antes del siguiente ciclo
        await asyncio.sleep(60)  # 1 minuto