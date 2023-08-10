from pydantic import BaseModel
from models.PyObjectId import PyObjectId


class Like(BaseModel):
    post_id: PyObjectId
    user_id: PyObjectId
