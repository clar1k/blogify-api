from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class CommentIn(BaseModel):
    content: str
    post_id: str
    token: str

class Comment(BaseModel):
    content: str
    user_id: ObjectId = Field(None) 
    post_id: str
    created_at: datetime = datetime.utcnow()
    
    class Config:
        arbitrary_types_allowed = True