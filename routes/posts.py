from fastapi import APIRouter

posts = APIRouter()


@posts.get('/{user_id}', tags=['Posts'])
def get_post_by_user(user_id: str):
    pass


@posts.get('/post/{post_id}', tags=['Posts'])
def get_post_by_id(post_id: str):
    pass


@posts.post('/post/', tags=['Posts'])
def create_post():
    pass


