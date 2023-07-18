from datetime import datetime
from pydantic import BaseModel, Field
from models.PyObjectId import PyObjectId


class Comment(BaseModel):
    content: str
    user_id: PyObjectId = None
    post_id: PyObjectId = None
    created_at: datetime = datetime.utcnow()


class CommentIn(BaseModel):
    token: str
    content: str
    post_id: PyObjectId


class CommentUpdate(BaseModel):
    content: str
