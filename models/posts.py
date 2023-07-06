from pydantic import BaseModel

class Post(BaseModel):
    user_id: str
    text: str