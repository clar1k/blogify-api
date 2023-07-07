from pydantic import BaseModel, Field, EmailStr
import bcrypt
import datetime


class User(BaseModel):
    nickname: str
    email: EmailStr
    password: bytes
    salt: bytes = b''
    is_confirm: bool = False
    created_at: datetime.datetime = datetime.datetime.now()


class UserIn(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    nickname: str
    email: EmailStr

def check_password(password: str, salt: bytes, hashed_pw: bytes) -> bool:
    hashed_input = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_input == hashed_pw