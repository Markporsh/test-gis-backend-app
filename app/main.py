from fastapi import FastAPI

from app.database import Base, engine
from app.routers import circle, users

app = FastAPI()

app.include_router(circle.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
