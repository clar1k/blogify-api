from pydantic import BaseModel
from models.PyObjectId import PyObjectId

class Follow(BaseModel):
    token: str
    author_id: PyObjectId