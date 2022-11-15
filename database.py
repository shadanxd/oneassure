from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.environ.get('username')
db_password = os.environ.get('password')


class DBHandler:

    cluster = MongoClient(f'mongodb+srv://{db_user}:{db_password}@cluster0.ef68wuq.mongodb.net/?retryWrites=true&w'
                          f'=majority')
    db = cluster["Cluster0"]
    collections = db["OneAssure"]

    @classmethod
    async def save(cls, item: dict):
        cls.collections.insert_one(item)

    @classmethod
    async def update_user_details(cls, scope: dict):
        if 'new_name' in scope:
            cls.collections.update_one({"username": scope['username']}, {"$set": {"name": scope['new_name']}})
        if 'new_number' in scope:
            cls.collections.update_one({"username": scope['username']}, {"$set": {"phone": scope['new_number']}})

    @classmethod
    async def getUserDetails(cls, username: str):
        user = cls.collections.find_one({"username": username},  {"_id": 0})
        if user is None:
            return None
        return user
