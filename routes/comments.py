from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.comments import Comment, CommentIn, CommentUpdate
from config.db import db
from models.posts import PostIn, PostUpdate
from utils.token import get_id
from bson import ObjectId
from schemas.comments import commentEntity, commentsEntity

comments = APIRouter(tags=["Comments"])


@comments.post("/comment/")
def post_comment(comment: CommentIn) -> JSONResponse:
    _id = get_id(comment.token)
    if db.user.find_one({"_id": _id}):
        new_comment = Comment.parse_obj(comment)
        new_comment.user_id = _id
        db.comments.insert_one(new_comment.dict())
        return JSONResponse({"message": "Added comment"}, 200)
    return JSONResponse({"message": "Bad request"}, 400)


@comments.get("/comments/post/{_id}")
def get_comments(unique_id: str) -> JSONResponse:
    if db.posts.find({"_id": ObjectId(unique_id)}):
        comments = db.comments.find({"post_id": unique_id})
        return JSONResponse(commentsEntity(comments), 200)
    return JSONResponse({"message": "Bad request"}, 400)


@comments.put("/comment/")
def update_comment(
    comment: CommentIn, post: PostUpdate, commentUpdate: CommentUpdate
) -> JSONResponse:
    find_post = db.posts.find_one(post.dict())
    if find_post:
        _filter = {"post_id": find_post["_id"]}
        update = {"$set": {"content": commentUpdate.content}}
        find_comment = db.comments.find_one_and_update(_filter, update)
        if find_comment:
            return JSONResponse({"message": "Success!"}, 200)
        return JSONResponse({"message": "Comment not found"}, 400)
    return JSONResponse({"message": "Post not found"}, 400)


@comments.delete("/comment/")
def delete_comment(comment: CommentIn) -> JSONResponse:
    post = db.posts.find_one({"_id": comment.post_id})
    if post:
        user_id = get_id(comment.token)
        _filter = {"content": comment.content, "user_id": user_id}
        if db.comments.find_one_and_delete(_filter):
            return JSONResponse({"message": "Comment deleted"}, 200)
        return JSONResponse({"message": "Comment not found"}, 400)
    return JSONResponse({"message": "Post not found"}, 400)
