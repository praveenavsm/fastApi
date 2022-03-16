from .. import models
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/")
def get_all_posts(db: Session = Depends(get_db), response_model=List[schemas.Post]):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    return posts


@router.get("/{id}")
def get_posts(id: int, db: Session = Depends(get_db), response_model=schemas.Post):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES ( %s, %s, %s ) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Posts(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if new_post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return new_post


@router.put("/{id}")
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_qry = db.query(models.Posts).filter(models.Posts.id == id)
    if post_qry.first() is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    post_qry.update(post.dict(), synchronize_session=False)
    db.commit()
    return post.first()


@router.delete("/{id}")
def delete_posts(id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    # cursor.execute("""DELETE FROM posts WHERE id =%s""",
    #                (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"update failed")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
