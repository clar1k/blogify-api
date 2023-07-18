from datetime import datetime
from pydantic import BaseModel
from models.PyObjectId import PyObjectId


class Post(BaseModel):
    author_id: PyObjectId = None
    title: str
    text: str
    likes: int = 0
    created_at: datetime = datetime.utcnow()


class PostIn(BaseModel):
    token: str
    title: str
    text: str


class PostUpdate(BaseModel):
    title: str
    text: str
