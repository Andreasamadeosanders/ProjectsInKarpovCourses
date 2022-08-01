from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func
from typing import List
from loguru import logger

from database import SessionLocal
from schema import UserGet, PostGet, FeedGet
from table_user import User
from table_post import Post
from table_feed import Feed

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(User) \
        .filter(User.id == id) \
        .one_or_none()
    if result is None:
        raise HTTPException(404, "user not found")
    else:
        return result


@app.get("/post/{id}", response_model=PostGet)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Post) \
        .filter(Post.id == id) \
        .one_or_none()
    if result is None:
        raise HTTPException(404, "user not found")
    else:
        return result


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed_by_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed) \
        .filter(Feed.user_id == id) \
        .order_by(Feed.time.desc()) \
        .limit(limit).all()
    return result


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_user_feed_by_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed) \
        .filter(Feed.post_id == id) \
        .order_by(Feed.time.desc()) \
        .limit(limit).all()
    return result


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_like_by_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Post) \
        .select_from(Feed) \
        .filter(Feed.action == "like") \
        .join(Post) \
        .group_by(Post.id) \
        .order_by(func.count(Post.id).desc()) \
        .limit(limit) \
        .all()
    return result