from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from app import database, schemas, models, utils

router = APIRouter(tags=['Authentication'])


@router.post('/auth')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

    # create token

    # return tokens
    return {"token": "Example token"}
