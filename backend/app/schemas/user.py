from pydantic import BaseModel, constr

class UserRegister(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)
    confirm_password: constr(min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
