import time
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from .routers import stores

app = FastAPI()


@app.get("/")
def root():
    return {"message": "welcome to my apis a"}


app.include_router(stores.router)



