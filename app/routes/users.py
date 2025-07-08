from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.config import (
    SessionLocal,
    get_password_hash, 
    verify_password, 
    create_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
    REFRESH_SECRET_KEY,
    decode_token,
    get_db,
    )
from app.schemas import UserCreate, Token
from app.models import User

user_router = APIRouter()

@user_router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(username=user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"msg": "User registered"}

@user_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password): # type: ignore
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access = create_token(
        {"sub": user.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        SECRET_KEY
    )
    refresh = create_token(
        {"sub": user.username},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        REFRESH_SECRET_KEY
    )
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@user_router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_token(refresh_token, REFRESH_SECRET_KEY)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload["sub"]
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access = create_token(
        {"sub": user.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        SECRET_KEY
    )
    new_refresh = create_token(
        {"sub": user.username},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        REFRESH_SECRET_KEY
    )
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

