from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import User
from config.db import conn
from schemas.user import usersEntity

user = APIRouter()


@user.get("/")
async def get_users():
    return await usersEntity(conn.blogify.user.find())


@user.post("/")
def create_user(user: User):
    if conn.blogify.user.find_one(dict(user)):
        return JSONResponse(
            content={"message": "User is already in database"}, status_code=400
        )
    conn.blogify.user.insert_one(dict(user))
    return JSONResponse({"message": "User has been created"}, status_code=201)
