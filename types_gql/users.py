import strawberry
from models.users import User, UserIn


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    email: strawberry.auto
    nickname: strawberry.auto
    created_at: strawberry.auto


@strawberry.experimental.pydantic.input(model=UserIn, all_fields=True)
class UserInType:
    pass
