import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32 or JWT_SECRET_KEY.startswith("replace_with_"):
    raise ValueError("Set JWT_SECRET_KEY to a random secret of at least 32 characters")

try:
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
except ValueError as exc:
    raise ValueError("JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer") from exc
if JWT_ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise ValueError("JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer")

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class TokenPrincipal:
    user_id: int
    role: str


def create_access_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user.id), "user_id": user.id, "role": user.role, "iat": now, "exp": expires_at},
        JWT_SECRET_KEY,
        algorithm="HS256",
    )


def decode_access_token(token: str) -> TokenPrincipal:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        role = payload.get("role")
        if (
            not isinstance(user_id, int)
            or user_id < 1
            or not isinstance(role, str)
            or role not in {"admin", "customer"}
        ):
            raise credentials_error
    except jwt.InvalidTokenError as exc:
        raise credentials_error from exc
    return TokenPrincipal(user_id=user_id, role=role)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    principal = decode_access_token(credentials.credentials)
    user = db.query(User).filter(User.id == principal.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
