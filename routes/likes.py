from config.db import db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.likes import Like
from bson import ObjectId
from utils.token import get_id
from schemas.likes import likesEntity
from schemas.posts import postEntity, postsEntity

likes = APIRouter(tags=["Likes"])


@likes.post("/like/post")
def like_post(like: Like):
    find_like_query = {"post_id": like.post_id}
    if db.likes.find_one(find_like_query, {"user_id": like.user_id}):
        decrement_like = {"$inc": {"likes": -1}}
        db.posts.find_one_and_update(
            {"_id": ObjectId(like.post_id)}, decrement_like)
        return JSONResponse({"message": "Unliked post"}, 200)
    db.likes.insert_one(like.dict())
    increment_like = {"$inc": {"likes": 1} }
    db.posts.find_one_and_update(find_like_query, increment_like)
    return JSONResponse({"message": "Liked post"}, 201)


@likes.get("/like/user/posts/{token}")
def get_liked_posts_by_user(token: str) -> JSONResponse:
    uid = get_id(token)
    if likes := db.likes.find({"user_id": ObjectId(uid)}):
        likes = likesEntity(likes)
        posts = []
        for like in likes:
            _id = like["post_id"]
            post = db.posts.find_one({"_id": ObjectId(_id)})
            posts.append(post)
        return JSONResponse(postsEntity(posts), 200)
    return JSONResponse({"message": "Invalid token"}, 400)
