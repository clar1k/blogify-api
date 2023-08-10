from typing import Dict, List
from bson import ObjectId
import strawberry
from strawberry.fastapi import GraphQLRouter
from types_gql.posts import PostType
from types_gql.users import UserInType, UserType
from models.users import User
from models.posts import Post
from config.db import db
from routes.auth import handle_register
from pprint import pprint


@strawberry.type
class Query:
    @strawberry.field
    def get_user(nickname: str) -> UserType:
        find_filter = {"nickname": nickname}
        user = db.user.find_one(find_filter)
        pydantic_user = User.parse_obj(user)
        user_type = UserType.from_pydantic(pydantic_user)
        if user:
            return user_type
        return "User not found"

    @strawberry.field
    def get_user_posts(nickname: str) -> List[PostType]:
        user_posts = find_user_posts_by_nickname(nickname)
        posts = list(user_posts)
        post_types = []
        for post in posts:
            post = Post.parse_obj(post)
            post_types.append(PostType.from_pydantic(post))
        if post_types:
            return post_types


def find_user_posts_by_nickname(nickname: str):
    find_user_filter = {"nickname": nickname}
    user: Dict = db.user.find_one(find_user_filter)
    return db.posts.find({"author_id": ObjectId(user["_id"])})


@strawberry.type
class Mutations:
    @strawberry.mutation
    async def register_user(user_input: UserInType) -> str:
        user_is_existed = db.user.find_one({"email": user_input.email})
        if user_is_existed:
            return "User is already registered"
        user = user_input.to_pydantic()
        await handle_register(user)
        return "User succesfully registered"


schema = strawberry.Schema(query=Query, mutation=Mutations)
graphql_app = GraphQLRouter(schema)
