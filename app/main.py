import time
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from . import models
from .routers import post, user, auth

from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='Ps!in4597')
#
#         cursor = conn.cursor()
#         print('Database connection was successfull')
#         break
#     except Exception as error:
#         print(f'Connection failed with error:{error}')
#         time.sleep(2)


@app.get("/")
def root():
    return {"message": "welcome to my apis a"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


