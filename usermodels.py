from pydantic import BaseModel, validator, StrictInt, StrictStr
from typing import Optional
from auth import AuthHandler


class UserBase(BaseModel):
    username: str = "John_Doe"
    name: StrictStr = "john123"
    phone: StrictInt = 1234
    type: Optional[str] = "Users"
    password: str

    class Config:
        anystr_strip_whitespace = True
        max_anystr_length = 20
        validate_all = True
        validate_assignment = True

    @validator('password')
    def hashing(cls, pwd):
        return AuthHandler.get_password_hash(pwd)


class UserUpdate(BaseModel):
    username: str
    name: Optional[StrictStr] = None
    phone: Optional[StrictInt] = None
    type: Optional[str] = "Users"

    class Config:
        anystr_strip_whitespace = True
        max_anystr_length = 20
        validate_all = True
        validate_assignment = True




