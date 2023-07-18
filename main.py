import uvicorn
from fastapi import FastAPI
from routes import posts, auth, comments, likes, follows, users

app = FastAPI(debug=True, title="Blogify")

app.include_router(auth.auth)
app.include_router(users.users)
app.include_router(posts.posts)
app.include_router(comments.comments)
app.include_router(likes.likes)
app.include_router(follows.follows)


if __name__=="__main__":
    uvicorn.run('main:app', reload=True)