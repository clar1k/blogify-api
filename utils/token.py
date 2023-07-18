import jwt
from bson import ObjectId
from config.config import Config
from datetime import datetime
from config.db import db


def get_id(token: str) -> ObjectId:
    token = jwt.decode(token,Config.SECRET_KEY, ['HS256'])
    _id = token['_id']
    _id = ObjectId(_id)
    return _id


def is_token_expired(decoded_token: dict) -> bool:
    expiration_time = decoded_token['exp']
    expiration_time = datetime.utcfromtimestamp(expiration_time)
    time_now = datetime.utcnow()
    if expiration_time < time_now:
        return True
    return False


def is_token_blacklisted(token: str) -> bool:
    _filter = {"token": token}
    if db.token_blacklist.find_one(_filter):
        return True
    return False