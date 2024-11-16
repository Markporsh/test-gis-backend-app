import os

ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mydatabase")
SECRET_KEY = os.getenv("SECRET_KEY", "some_secret_key")
ALGORITHM = "HS256"

