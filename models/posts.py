from datetime import datetime
from pydantic import BaseModel
class Post(BaseModel):
    author_id: str = ''
    title: str
    text: str
    likes: int = 0
    created_at: datetime = datetime.utcnow()

class PostIn(BaseModel):
    token: str
    title: str
    text: str