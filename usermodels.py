from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str = "John_Doe"
    name: str = "john123"
    phone: int = "1234"
    description: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
