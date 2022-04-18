from datetime import datetime
from typing import List

from pydantic import BaseModel 
from pydantic_mongo import ObjectIdField
from bson import ObjectId

class StoreBase(BaseModel):
    id: ObjectIdField = None
    store_nbr: int
    prgm_incl: List[int] = None

    class Config:
        # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectId: str}