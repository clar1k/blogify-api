from datetime import datetime
from pydantic import BaseModel, Field
from models.PyObjectId import PyObjectId

class CommentIn(BaseModel):
    content: str
    post_id: PyObjectId
    token: str

class Comment(BaseModel):
    content: str
    user_id: PyObjectId
    post_id: PyObjectId
    created_at: datetime = datetime.utcnow()