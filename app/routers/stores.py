from sys import set_coroutine_origin_tracking_depth
from fastapi import APIRouter , HTTPException, status
from ..schemas import StoreBase
from typing import List
from ..mongodatabase import store_repository

router = APIRouter(
    prefix="/stores",
    tags=['Stores']
)

@router.get("/", response_model=List[StoreBase])
def get_all_stores():
    results = store_repository.find_by({})
    store_list = list(results)
    return store_list


@router.post("/")
def get_all_stores(store_req_body: StoreBase):
    print(f" store {store_req_body.store_nbr}")
    store = store_repository.find_one_by({'store_nbr':int(store_req_body.store_nbr)})
    if store is None:
        store_post = store_repository.save(store_req_body)
        store = store_req_body
        store.id = store_post.inserted_id
        return store
        
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Store number already exists")
# # Insert / Update
# spam_repository.save(spam)

# # Delete
# spam_repository.delete(spam)

# # Find One By Id
# result = spam_repository.find_one_by_id(spam.id)

# # Find One By Query
# result = spam_repository.find_one_by({'foo.count': 1})

# # Find By Query
# results = spam_repository.find_by({'foo.count': {'$gte': 1}})