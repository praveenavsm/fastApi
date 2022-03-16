from datetime import datetime, timedelta

from jose import JWTError, jwt

# SECRET KEY
# Algorithm
# Expiration time

SECRET_KEY = "32890s8f90sdf9f8ds9f80s9d8f9s8f09sd8f9sd8f9sd8f9sd8f90sd89f0s8fsf9sd8f9"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
