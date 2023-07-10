import uvicorn
from fastapi import FastAPI
from routes import user, posts, auth, comments, likes

app = FastAPI(debug=True)
app.include_router(user.user)
app.include_router(posts.posts)
app.include_router(auth.auth)
app.include_router(comments.comments)
app.include_router(likes.like)

if __name__=="__main__":
    uvicorn.run('main:app', reload=True)