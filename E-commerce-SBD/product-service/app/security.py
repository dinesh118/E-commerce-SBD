import os
from dataclasses import dataclass

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32 or JWT_SECRET_KEY.startswith("replace_with_"):
    raise ValueError("Set JWT_SECRET_KEY to the same random secret used by Auth Service")

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class TokenPrincipal:
    user_id: int
    role: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> TokenPrincipal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        role = payload.get("role")
        if (
            not isinstance(user_id, int)
            or user_id < 1
            or not isinstance(role, str)
            or role not in {"admin", "customer"}
        ):
            raise ValueError("Invalid token claims")
    except (jwt.InvalidTokenError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenPrincipal(user_id=user_id, role=role)
