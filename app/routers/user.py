from .. import schemas, utils
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password which is in user.password
    hashed_password = utils.hash_pwd(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f"User already exists")
    if new_user is None:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Create failed")
    return new_user


@router.get("/{id}", response_model=schemas.User)
def get_user_by_id(id1: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id1).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id1} not found")
    return user
