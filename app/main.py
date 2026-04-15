import asyncio
from fastapi import FastAPI

from app.routes import file_routes
from app.tasks.background_tasks import cleanup_expired_files

app = FastAPI()

app.include_router(file_routes.router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_expired_files())


from app.database.connection import engine

try:
    conn = engine.connect()
    print("Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print("Error:", e)