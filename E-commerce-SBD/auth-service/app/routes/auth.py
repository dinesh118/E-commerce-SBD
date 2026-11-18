from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserLogin, UserRegister, UserResponse
from app.security import create_access_token, get_current_user
from app.services.auth_service import login_admin, login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user_data.username, user_data.password, user_data.confirm_password)
    return user


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = login_user(db, user_data.username, user_data.password)
    return {"access_token": create_access_token(user), "user": user}


@router.post("/admin-login", response_model=TokenResponse)
def admin_login(login_info: UserLogin, db: Session = Depends(get_db)):
    user = login_admin(db, login_info.username, login_info.password)
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
