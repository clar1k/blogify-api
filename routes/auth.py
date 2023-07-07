from fastapi import APIRouter
from fastapi.responses import JSONResponse
import bcrypt
import jwt
from models.user import UserIn, User, check_password
from models.token import Token
from config.db import db

auth = APIRouter()


@auth.post('/auth/register', tags=['Auth'])
def register(user: UserIn) -> JSONResponse:
    if db.user.find_one({"email":user.email}):
        return JSONResponse({"message":"User is already in the database"}, 400)
    salt: bytes = bcrypt.gensalt()
    user.password = bcrypt.hashpw(user.password.encode(),salt=salt)
    new_user = User.parse_obj(user) #* Takes all the fields from the json body
    new_user.salt = salt
    db.user.insert_one(new_user.dict())
    return JSONResponse({"message":"User successfully registered"},
    200)


@auth.post('/auth/login', tags=['Auth'])
def login(user_input: UserIn):
    user = db.user.find_one({"email":user_input.email})
    if user:
        if check_password(user_input.password,user['salt'],user['password']):
            token = jwt.encode({"obj_id":str(user['_id'])},'secret_key')
            return JSONResponse({"access_token":token,"message":"Success!"}, 200)
        return JSONResponse({"message":"Incorrect password"}, 400)
    return JSONResponse({"message":"User is not registered"}, 400)


@auth.post('/auth/logout/', tags=['Auth'])
def logout(token: Token):
    if db.token_blacklist.find_one({"token":str(token)}):
        return JSONResponse({"message":"Token is already in the database"}, 400)
    db.token_blacklist.insert_one({"token":str(token)})
    return JSONResponse({"message":"Logout successful"}, 200)