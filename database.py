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
    async def update(cls, update_fields: dict, collection):
        collections = cls.db[f'{collection}']
        collections.update_one({"username": update_fields['username']}, {"$set": update_fields})

    @classmethod
    async def fetch(cls, username: str, collection, excluded_fields: dict):
        collections = cls.db[f'{collection}']
        user = collections.find_one({"username": username},  excluded_fields)
        if user is None:
            return None
        return user

    @classmethod
    async def delete(cls, username: str, collection):
        collections = cls.db[f'{collection}']
        collections.delete_one({"username": username})
