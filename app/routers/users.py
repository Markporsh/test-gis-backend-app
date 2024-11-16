from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models.users import User
from app.schemas.users_request import UserRead, UserCreate, Token
from app.services.auth import pwd_context, authenticate_user, create_access_token
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    db_user = db.query(User).filter(
        (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение списка пользователей"""
    return db.query(User).offset(skip).limit(limit).all()


@router.post("/token/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    """
    Получение токена пользователем. Токен действует 30 минут
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
