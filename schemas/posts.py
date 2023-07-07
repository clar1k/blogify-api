def postEntity(post: dict) -> dict:
    return {
        "text": post['text'],
        "author_id": post['author_id']
    }

def postsEntity(posts) -> list:
    return [postEntity(post) for post in posts]