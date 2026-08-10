from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.database.connection import get_db
from app.services.auth_service import register_user, login_user, login_admin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user_data.username, user_data.password, user_data.confirm_password)
    return user


@router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = login_user(db, user_data.username, user_data.password)
    return user


@router.post("/admin-login")
def admin_login(login_info: UserLogin):
    login_admin(login_info.username, login_info.password)
    return {"message": "Admin login successful"}
