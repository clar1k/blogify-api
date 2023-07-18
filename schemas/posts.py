def postEntity(post: dict) -> dict:
    return {
        "title": post["title"],
        "text": post["text"],
        "author_id": post["author_id"],
    }


def postsEntity(posts: list) -> list:
    return [postEntity(post) for post in posts]
