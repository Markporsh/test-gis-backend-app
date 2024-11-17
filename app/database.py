from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session
