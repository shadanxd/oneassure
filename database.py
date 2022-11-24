import os
from pymongo import MongoClient
from dotenv import load_dotenv


class DBHandler:

    load_dotenv()
    username = os.getenv('username')
    password = os.getenv('password')
    host = os.getenv('db_host')
    user_type = os.getenv('user_type')
    cluster = MongoClient(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w'
                          f'=majority')
    db = cluster["Cluster0"]
    collections = db[f'OneAssure{user_type}']

    @classmethod
    async def save(cls, item: dict):
        user_type = item['type']
        collections = cls.db[f'OneAssure{user_type}']
        collections.insert_one(item)

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
