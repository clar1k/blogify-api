import jwt
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from bson import ObjectId
from models.posts import PostIn, Post
from config.db import db
from schemas.posts import postEntity, postsEntity

posts = APIRouter()


@posts.get('/post/user/{user_id}', tags=['Posts'])
def get_post_by_user(user_id: str) -> JSONResponse:
    if posts := db.posts.find({"author_id":user_id}):
        return JSONResponse(postsEntity(posts), 200)
    return JSONResponse({"message":"Posts not found"},400)


@posts.get('/post/{post_id}', tags=['Posts'])
def get_post_by_id(post_id: str):
    if post := db.posts.find_one({"_id":ObjectId(post_id)}):
        return JSONResponse(postEntity(post), 200)
    return JSONResponse({"message":"There`s no post by this id"}, 400)


@posts.post('/post/', tags=['Posts'])
def create_post(post: PostIn) -> JSONResponse:
    token_decode = jwt.decode(post.token.encode('utf-8'),'secret_key', algorithms=['HS256'])
    _id = token_decode['_id']
    new_post: Post = Post.parse_obj(post)
    new_post.author_id = str(_id)
    db.posts.insert_one(new_post.dict())
    return JSONResponse({"message":"Post succesfulyy created"}, 201)


@posts.delete('/post/{post_id}', tags=['Posts'])
def delete_post_by_id(post_id: str) -> JSONResponse:
    if db.posts.find_one_and_delete({"_id":ObjectId(post_id)}):
        return JSONResponse({"message":"Post was deleted"}, 200)
    return JSONResponse({"message":"Post not found"}, 400)


@posts.put('/post')
def update_post() -> JSONResponse:
    return