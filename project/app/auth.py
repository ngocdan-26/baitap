
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key-before-deployment"
)
ALGORITHM = "HS256"
EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user.id),
        "role": user.role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    error = HTTPException(
        status_code=401,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = int(payload.get("sub", "0"))
    except (jwt.InvalidTokenError, ValueError, TypeError) as exc:
        raise error from exc

    user = db.get(User, user_id)
    if not user:
        raise error
    return user


def admin_only(
    user: User = Depends(get_current_user)
) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền thực hiện chức năng này"
        )

    return user
