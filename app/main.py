from fastapi import FastAPI
from app.routers import circle, users

app = FastAPI()

app.include_router(circle.router)
app.include_router(users.router)
