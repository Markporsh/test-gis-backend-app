from datetime import datetime, timezone, timedelta
from typing import Union, Optional

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.settings import SECRET_KEY, ALGORITHM
from app.models.users import User
from app.schemas.users_request import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, username: str) -> Optional[UserInDB]:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Union[bool, UserInDB]:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Создаем токен для пользователя.
    Если не передать expires_delta, то токен действует 15 минут
    """
    to_encode = data.copy()
    expires_delta = timedelta(minutes=15) if expires_delta is None else expires_delta
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(token: str, secret_key: str, algorithms: list) -> None:
    """Проверка валидности токена"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Недействительные учетные данные")
    except JWTError:
        raise HTTPException(status_code=401, detail="Недействительные учетные данные")
