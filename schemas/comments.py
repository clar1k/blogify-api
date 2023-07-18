def commentEntity(comment: dict) -> dict:
    return {"content": comment["content"]}


def commentsEntity(comments: list) -> list:
    return [commentEntity(comment) for comment in comments]
