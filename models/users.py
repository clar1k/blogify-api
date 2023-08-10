from datetime import datetime
import bcrypt
from pydantic import BaseModel, EmailStr
from models.PyObjectId import PyObjectId
from typing import List


class User(BaseModel):
    nickname: str
    email: EmailStr
    password: bytes
    salt: bytes = b""
    is_confirm: bool = False
    confirm_token: str = ""
    image_filename: str = ""
    followers: List[PyObjectId] = []
    created_at: datetime = datetime.utcnow()


class UserIn(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    nickname: str
    email: EmailStr


def check_password(password: str, salt: bytes, hashed_password: bytes) -> bool:
    hashed_input = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_input == hashed_password
