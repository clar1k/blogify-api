import uvicorn
from fastapi import FastAPI
from routes import posts, auth, comments, likes, follows, users
from gql import graphql_app

app = FastAPI(debug=True, title="Blogify")

app.include_router(auth.auth)
app.include_router(users.users)
app.include_router(posts.posts)
app.include_router(comments.comments)
app.include_router(likes.likes)
app.include_router(follows.follows)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
