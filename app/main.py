from fastapi import FastAPI
from app.routes import file_routes

app = FastAPI()

app.include_router(file_routes.router)

from app.database.connection import engine

try:
    conn = engine.connect()
    print("Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print("Error:", e)