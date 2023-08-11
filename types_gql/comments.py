import strawberry
from models.comments import Comment


@strawberry.experimental.pydantic.type(model=Comment)
class CommentType:
    content: strawberry.auto
    created_at: strawberry.auto
