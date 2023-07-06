from pydantic import BaseModel, Field, EmailStr
import datetime


class User(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    salt: str = ""
    created_at: datetime.datetime = datetime.datetime.now()
    image: bytes = Field(..., description="Profile picture as binary data")


class UserIn(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    image: bytes = Field(..., description="Profile picture as binary data")


class UserOut(BaseModel):
    nickname: str
    email: EmailStr
    image: bytes = Field(..., description="Profile picture as binary data")
