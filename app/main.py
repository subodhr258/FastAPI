# venv\Scripts\activate.bat
# uvicorn app.main:app --reload
#sqlalchemy is one of the most popular ORMs. It can be used with any framework.

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine,get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="1234",
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Successful")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print("Error:",error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") #route or path operation decorator
async def root(): #async needed?
    return {"message":"Welcome to my API..."}

