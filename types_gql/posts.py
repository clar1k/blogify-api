import strawberry
from models.posts import Post


@strawberry.experimental.pydantic.type(model=Post)
class PostType:
    title: strawberry.auto
    text: strawberry.auto
    likes: strawberry.auto


@strawberry.experimental.pydantic.input(model=Post)
class PostInputType:
    title: strawberry.auto
    text: strawberry.auto
