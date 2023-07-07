from pydantic import BaseModel

class Post(BaseModel):
    author_id: str = ''
    text: str
    likes: int = 0

class PostIn(BaseModel):
    token: str
    text: str