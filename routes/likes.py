from config.db import db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.likes import Like
from bson import ObjectId
from utils.token import get_id 
from schemas.likes import likesEntity
from schemas.posts import postEntity,postsEntity
like = APIRouter(tags=['Likes'])


@like.post('/like/post')
def like_post(like: Like):
    if db.likes.find_one({"post_id":like.post_id, "user_id": like.user_id}):
        db.likes.find_one_and_delete(like.dict())
        db.posts.find_one_and_update( 
            {"_id":ObjectId(like.post_id)}, 
            {"$inc": {"likes": -1}}
        )
        return JSONResponse({"message":"Unliked"}, 200)
    
    db.likes.insert_one(like.dict())
    db.posts.find_one_and_update( 
            {"_id":ObjectId(like.post_id)}, 
            {"$inc": {"likes": 1}}
        )
    return JSONResponse({"message":"Liked"}, 201)


@like.get('/like/user/posts/{token}')
def get_liked_posts_by_user(token: str) -> JSONResponse:
    uid = get_id(token)
    if likes := db.likes.find({"user_id": ObjectId(uid)}):
        likes = likesEntity(likes)
        posts = []
        for like in likes:
            _id = like["post_id"]
            post = db.posts.find_one({"_id":ObjectId(_id)})
            posts.append(post)
        return JSONResponse(postsEntity(posts), 200)
    return JSONResponse({"message":"Invalid token"}, 400)
