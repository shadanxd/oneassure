import os
from pymongo import MongoClient
from dotenv import load_dotenv


class DBHandler:

    load_dotenv()
    username = os.getenv('username')
    password = os.getenv('password')
    host = os.getenv('db_host')
    cluster = MongoClient(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w'
                          f'=majority')
    db = cluster["Cluster0"]

    @classmethod
    async def save(cls, user: dict, collection_name: str):
        collections = cls.db[f'{collection_name}']
        collections.insert_one(user)

    @classmethod
    async def update_user_details(cls, scope: dict, collection):
        collections = cls.db[f'{collection}']
        if 'new_name' in scope:
            collections.update_one({"username": scope['username']}, {"$set": {"name": scope['new_name']}})
        if 'new_number' in scope:
            collections.update_one({"username": scope['username']}, {"$set": {"phone": scope['new_number']}})

    @classmethod
    async def getUserDetails(cls, username: str, collection):
        collections = cls.db[f'{collection}']
        user = collections.find_one({"username": username},  {"_id": 0})
        if user is None:
            return None
        return user
