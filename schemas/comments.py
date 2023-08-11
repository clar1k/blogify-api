def commentEntity(comment: dict) -> dict:
    return {"content": comment["content"], "created_at": comment["created_at"]}


def commentsEntity(comments: list) -> list:
    return [commentEntity(comment) for comment in comments]
