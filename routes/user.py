from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserIn, User
from config.db import db
from schemas.user import userEntity
from bson import ObjectId
import bcrypt
import jwt

user = APIRouter()


@user.get("/{user_id}", tags=["users"])
def get_user(user_id: str):
    _id = ObjectId(user_id)
    user = db.user.find_one({"_id": _id})
    return userEntity(user)


@user.post("/", tags=["users"])
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


@user.post("/login", tags=["users"])
def login_user(user: UserIn):
    log_user = db.user.find_one({"email": user.email})
    password = user.password.encode("utf-8")

    passw = bcrypt.hashpw(password, log_user["salt"])
    if passw == log_user["password"]:
        payload = {"user_id": str(log_user["_id"])}
        token = jwt.encode(payload=payload,key="SECRET_KEY")
        return JSONResponse(
            {"message": "User logged in", "token": token}, status_code=200
        )
    return JSONResponse({"message": "Invalid arguments"}, 400)


@user.put("/", tags=["users"])
def update_user(user: UserIn):
    pass
