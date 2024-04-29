from pymongo import MongoClient
from config import MONGODB_URI


class MongoDBClient:
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            client = MongoClient(MONGODB_URI)
            cls.instance = client["sample_mflix"]
        return cls.instance

    def get_db(cls):
        return cls.instance
