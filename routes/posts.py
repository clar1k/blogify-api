from fastapi import APIRouter

posts = APIRouter()


@posts.get('/{user_id}')
def get_post_by_user(user_id: str):
    pass


@posts.post('/post/')
def create_post():
    pass


@posts.get('/post/{post_id}')
def get_post_by_id(post_id: str):
    pass