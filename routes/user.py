import jwt
import bcrypt
from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Body
from models.user import UserIn, User, UserUpdate
from config.db import db
from config.config import Config
from schemas.user import userEntity

user = APIRouter(tags=['Users'])


@user.get("/user/{user_id}")
def get_user(user_id: str):
    _id = ObjectId(user_id)
    user = db.user.find_one({"_id": _id})
    return userEntity(user)


@user.post("/user")
def create_user(user: UserIn):
    if db.user.find_one(dict(user)):
        return JSONResponse({"message": "User is already in database"},
        status_code=400)
    new_user = User.parse_obj(user)
    new_user.salt = bcrypt.gensalt()
    salt = new_user.salt
    password = new_user.password.encode()  # *Encoded to the binary data
    new_user.password = bcrypt.hashpw(password, salt)
    db.user.insert_one(new_user.dict())
    return JSONResponse({"message": "User has been created"}, status_code=201)


@user.put("/user")
def update_user(user: UserUpdate):
    if db.user.find_one_and_replace({"email": user.email}, user.dict()):
        return JSONResponse({"message":"Update successfull :D"}, 201)
    return JSONResponse({"message":"Invalid value :( "}, 400)


@user.delete("/user")
async def delete_user(token: dict = Body(..., example={"token":"access token value"})):
    decoded_token = jwt.decode(token['token'], Config.SECRET_KEY, ['HS256'])
    _id = ObjectId(decoded_token['_id'])
    if db.user.find_one_and_delete({"_id":_id}):
        return JSONResponse({"message":"Success!"}, 200)
    return JSONResponse({"message":"User does not exist"}, 400)