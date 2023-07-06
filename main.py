import uvicorn
from fastapi import FastAPI
from routes.user import user
from routes.posts import posts

app = FastAPI(debug=True)
app.include_router(user)
app.include_router(posts)


if __name__=="__main__":
    uvicorn.run('main:app', reload=True)