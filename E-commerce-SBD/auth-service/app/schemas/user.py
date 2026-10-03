from pydantic import BaseModel, ConfigDict, constr


class UserRegister(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)
    confirm_password: constr(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
