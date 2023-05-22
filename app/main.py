from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='lessgoReal@14Ucl', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as err:
        print("databse conncetion failed")
        print("error:", err)
        time.sleep(5)

my_posts = [{"title": "title 1", "content": "content 1", "id": 1}, {"title": "title 2", "content": "content 2", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "lets build cloud"}
