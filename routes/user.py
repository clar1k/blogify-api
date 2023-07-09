import bcrypt
from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserIn, User
from config.db import db

from schemas.user import userEntity

user = APIRouter()


@user.get("/{user_id}", tags=["Users"])
def get_user(user_id: str):
    _id = ObjectId(user_id)
    user = db.user.find_one({"_id": _id})
    return userEntity(user)


@user.post("/", tags=["Users"])
def create_user(user: UserIn):
    if db.user.find_one(dict(user)):
        return JSONResponse({"message": "User is already in database"},
        status_code=400)
    new_user = User.parse_obj(user)
    
    new_user.salt = bcrypt.gensalt()
    salt = new_user.salt
    password = new_user.password.encode("utf-8")  # *Encoded to the binary data
    new_user.password = bcrypt.hashpw(password, salt)
    db.user.insert_one(new_user.dict())
    return JSONResponse({"message": "User has been created"}, status_code=201)


@user.put("/", tags=["Users"])
def update_user(user: UserIn):
    pass


@user.delete("/", tags=["Users"])
def delete_user():
    return