import pymongo
from .schemas import StoreBase
from pydantic_mongo import AbstractRepository

client = pymongo.MongoClient("mongodb+srv://praveenavsm:suDPIDRtkgSeNb3S@cluster0.ldajt.mongodb.net/patientdb"
                             "?retryWrites=true&w=majority&tls=true" , tlsAllowInvalidCertificates=True)

mydb = client['patientdb']

class StoreRepository(AbstractRepository[StoreBase]):
    class Meta:
        collection_name = 'stores'

store_repository = StoreRepository(database=mydb)
