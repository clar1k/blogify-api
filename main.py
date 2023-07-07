import uvicorn
from fastapi import FastAPI
from routes import user, posts, auth

app = FastAPI(debug=True)
app.include_router(user.user)
app.include_router(posts.posts)
app.include_router(auth.auth)

if __name__=="__main__":
    uvicorn.run('main:app', reload=True)