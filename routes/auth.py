import io
import asyncio
from datetime import datetime, timedelta
import bcrypt
import jwt
from PIL import Image
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
from models.user import UserIn, User, check_password 
from config.db import db
from config.mail import send_message, generate_confirm_token, get_email_by_token
from config.config import Config

auth = APIRouter(tags=['Auth'])


@auth.post('/auth/register')
async def register(user: UserIn, background_tasks: BackgroundTasks) -> JSONResponse:
    if db.user.find_one({"email":user.email}):
        return JSONResponse({"message":"User is already in the database"}, 400)
    background_tasks.add_task(handle_user_input, user)
    return JSONResponse({"message":"User successfully registered, confirm your email!"}, 201)


async def handle_user_input(user: UserIn):
    salt: bytes = bcrypt.gensalt()
    user.password: bytes = bcrypt.hashpw(user.password.encode(),salt=salt)
    new_user = User.parse_obj(user)
    new_user.salt = salt
    
    token = generate_confirm_token(new_user.email)
    new_user.confirm_token = token
    send_message(new_user.email, token)
    db.user.insert_one(new_user.dict())
    print(datetime.utcnow())


@auth.post('/auth/login')
def login(user_input: UserIn) -> JSONResponse:
    if user := db.user.find_one({"email":user_input.email}):
        if check_password(user_input.password,user['salt'],user['password']):
            _id = str(user['_id'])
            expiration_time = datetime.utcnow() + timedelta(days=2)
            token = jwt.encode(
                {
                "_id":_id,
                "exp":expiration_time,
                }, Config.SECRET_KEY)
            return JSONResponse({"access_token":token,"message":"Success!"}, 200)
        return JSONResponse({"message":"Incorrect password"}, 400)
    return JSONResponse({"message":"User is not registered"}, 400)


@auth.post('/auth/logout/{token}')
def logout(token: str) -> JSONResponse:
    if db.token_blacklist.find_one({"token":token}):
        return JSONResponse({"message":"Token is already in the database"}, 400)
    db.token_blacklist.insert_one({"token":token})
    return JSONResponse({"message":"Logout successful"}, 200)


@auth.put('/confirm/{token}')
def confirm_email(token: str):
    email = get_email_by_token(token)
    if db.user.find_one_and_update({"email":email},{"$set":{"is_confirm":True}},return_document=True):
        return JSONResponse({"message":"User activated the account"}, 200)
    return JSONResponse({"message":"Invalid request"}, 400)


@auth.put('/auth/register')
async def upload_avatar(file: UploadFile = File(...)):
    bytes_img = io.BytesIO(await file.read())
    img = Image.open(bytes_img)
    upload_path = Config.UPLOAD_FOLDER + file.filename
    img.save(upload_path, 'JPEG')
    return JSONResponse({"message":"Success"}, 201)