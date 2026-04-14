from fastapi import FastAPI
from app.routes import file_routes

app = FastAPI()

app.include_router(file_routes.router)