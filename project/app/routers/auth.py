
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, Token
from app.auth import (
    hash_password, verify_password,
    create_token, get_current_user
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/setup-admin", status_code=201)
def setup_admin(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    if db.scalar(
        select(User.id).where(User.role == "ADMIN")
    ):
        raise HTTPException(403, "ADMIN đã tồn tại")

    if db.scalar(
        select(User.id).where(User.username == data.username)
    ):
        raise HTTPException(400, "Username đã tồn tại")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role="ADMIN"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Tạo ADMIN thành công",
        "id": user.id,
        "username": user.username
    }


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.scalar(
        select(User).where(User.username == form.username)
    )

    if not user or not verify_password(
        form.password, user.password_hash
    ):
        raise HTTPException(
            401,
            "Sai username hoặc password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": create_token(user),
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
