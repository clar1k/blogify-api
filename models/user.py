import datetime
import bcrypt
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    nickname: str
    email: EmailStr
    password: bytes
    salt: bytes = b''
    is_confirm: bool = False
    confirm_token: str = ''
    image_filename: str = ''
    created_at: datetime.datetime = datetime.datetime.now()


class UserIn(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    nickname: str
    email: EmailStr


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    email: EmailStr
    password: Optional[str] = None
    
def check_password(password: str, salt: bytes, hashed_pw: bytes) -> bool:
    hashed_input = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_input == hashed_pw