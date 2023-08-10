from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.follows import Follow
from utils.token import get_id
from config.db import db

follows = APIRouter(tags=["Follows"])


@follows.post("/follow/user")
def follow(follow: Follow) -> JSONResponse:
    unique_id = get_id(follow.token)
    if db.user.find_one({"_id": unique_id}):

        if db.user.find_one_and_update(
            {"followers": {"$in": [unique_id]}}, {"$unset": {"followers": unique_id}}
        ):
            return JSONResponse({"message": "Unfollowed"}, 400)

        if db.user.find_one_and_update(
            {"_id": follow.author_id},
            {
                "$push": {
                    "followers": unique_id,
                }
            },
        ):
            return JSONResponse({"message": "Followed"}, 200)
    return JSONResponse({"message": "User not found"}, 400)


@follows.get("/follow/user/{unique_id}")
def get_user_followers(unique_id: str) -> JSONResponse:
    if user := db.user.find_one({"_id": ObjectId(unique_id)}):
        return JSONResponse({"followers": str(list(user["followers"]))}, 200)
    return JSONResponse({"message": "User is not registered"}, 400)
