from pydantic import BaseModel, validator, StrictInt, StrictStr
from typing import Optional
from auth import AuthHandler
from pydantic.dataclasses import dataclass


class UserBase(BaseModel):
    name: Optional[StrictStr] = "John Doe"
    phone: Optional[StrictInt] = "1234"
    type: Optional[str] = "Users"

    class Config:
        max_anystr_length = 20
        validate_all = True
        error_msg_templates = {
            'value_error.any_str.max_length': 'max_length:{limit_value}',
        }


class UserCred(UserBase):
    username: str = "john_Doe"
    password: str = "password"

    @validator('password')
    def hashing(cls, pwd):
        return AuthHandler.get_password_hash(pwd)





