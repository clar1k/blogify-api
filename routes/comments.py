from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.comments import Comment, CommentIn
from config.db import db
from utils.token import get_id
from bson import ObjectId
from schemas.comments import commentEntity, commentsEntity

comments = APIRouter(tags=['Comments'])


@comments.post('/comment')
def post_comment(comment: CommentIn) -> JSONResponse:
    _id = get_id(comment.token)
    if db.user.find_one({"_id":_id}):
        new_comment = Comment.parse_obj(comment)
        new_comment.user_id = _id
        db.comments.insert_one(new_comment.dict())
        return JSONResponse({"message":"Added comment"}, 200)
    return JSONResponse({"message":"Bad request"}, 400)


@comments.get('/post/comments/{_id}')
def get_comments(_id: str) -> JSONResponse:
    if db.posts.find({"_id":ObjectId(_id)}):
        comments = db.comments.find({"post_id":_id})
        return JSONResponse(commentsEntity(comments), 200)
    return JSONResponse({"message":"Bad request"}, 400)