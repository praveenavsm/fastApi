from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/auth')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return tokens
    return {"access_token": access_token, "token_type": "bearer"}
