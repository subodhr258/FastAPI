# venv\Scripts\activate.bat
# uvicorn app.main:app --reload
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# settings.database_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"])

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") #route or path operation decorator
async def root(): #async needed?
    return {"message":"Welcome to my API..."}

