from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db),
                  current_user=Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    new_post = models.Posts(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if new_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return new_post


@router.put("/{upd_id}", response_model=schemas.Post)
def update_posts(upd_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    post_qry = db.query(models.Posts).filter(models.Posts.id == upd_id)
    post_from_db = post_qry.first()
    if post_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    if post_from_db.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not authorized to update another owner's post")
    post_qry.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_from_db


@router.delete("/{delete_id}")
def delete_posts(delete_id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT,
                 current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == delete_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"update failed")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not authorized to delete another owner's post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
