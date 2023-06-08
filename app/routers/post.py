from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published) )
    # newpost = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    newpost = models.Post(owner_id=current_user.id, **post.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id = %s""", (str(id)))
    # post = cursor.fetchone()
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return post

@router.delete("/{id}", status_code=204)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = 404, detail=f"post with id: {id} does not exist")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=204)

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""", (post.title, post.content, post.published, str(id)))
    # update_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code = 404, detail=f"post with id: {id} does not exist")
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
