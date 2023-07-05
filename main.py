from fastapi import FastAPI
from routes.user import user

app = FastAPI(debug=True)
app.include_router(user)
