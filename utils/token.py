import jwt
from bson import ObjectId
from config.config import Config


def get_id(token: str) -> ObjectId:
    token = jwt.decode(token,Config.SECRET_KEY, ['HS256'])
    _id = token['_id']
    _id = ObjectId(_id)
    return _id