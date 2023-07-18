def likeEntity(like: dict) -> dict:
    return {"post_id": like["post_id"]}


def likesEntity(likes: list) -> list:
    return [likeEntity[like] for like in likes]
