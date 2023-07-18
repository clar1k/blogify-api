from fastapi import APIRouter
from fastapi.responses import JSONResponse
from bson import ObjectId
from models.posts import PostIn, Post, PostUpdate
from config.db import db
from schemas.posts import postEntity, postsEntity
from utils.token import get_id

posts = APIRouter(tags=["Posts"])


@posts.get("/post/user/{user_id}")
def get_post_by_user(user_id: str) -> JSONResponse:
    if posts := db.posts.find({"author_id": user_id}):
        return JSONResponse(postsEntity(posts), 200)
    return JSONResponse({"message": "Posts not found"}, 400)


@posts.get("/post/{post_id}")
def get_post_by_id(post_id: str):
    if post := db.posts.find_one({"_id": ObjectId(post_id)}):
        return JSONResponse(postEntity(post), 200)
    return JSONResponse({"message": "There`s no post by this id"}, 400)


@posts.post("/post/")
def create_post(post: PostIn) -> JSONResponse:
    _id = get_id(post.token)
    new_post: Post = Post.parse_obj(post)
    new_post.author_id = _id
    db.posts.insert_one(new_post.dict())
    return JSONResponse({"message": "Post succesfulyy created"}, 201)


@posts.delete("/post/")
async def delete_post_by_title_and_text(post: PostIn) -> JSONResponse:
    _id = get_id(post.token)
    post_filter = {"title": post.title, "text": post.text, "author_id": _id}
    is_post_deleted = db.posts.find_one_and_delete(post_filter)
    if is_post_deleted:
        return JSONResponse({"message": "Post deleted"}, 200)
    
    return JSONResponse({"message": "Post not found"}, 400)


@posts.put("/post/")
def update_post(post: PostIn, post_update: PostUpdate) -> JSONResponse:
    _id = get_id(post.token)
    _filter = {"title": post.title, "text": post.text, "author_id": _id}
    update = {"$set": {"title": post_update.title, "text": post_update.text}}
    if db.posts.find_one_and_update(_filter, update):
        return JSONResponse({"message": "Post updated"}, 200)
    return JSONResponse({"message": "Post not found"}, 400)
