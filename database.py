import os
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional


class DBHandler:

    load_dotenv()
    username = os.getenv('username')
    password = os.getenv('password')
    host = os.getenv('db_host')
    cluster = MongoClient(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w'
                          f'=majority')
    db = cluster["Cluster0"]

    @classmethod
    async def save(cls, items: list, collection_name: str):
        collections = cls.db[f'{collection_name}']
        collections.insert_many(items)

    @classmethod
    async def update(cls, query: dict, update_fields: dict, collection):
        collections = cls.db[f'{collection}']
        collections.update_many(query, {"$set": update_fields})

    @classmethod
    async def fetch(cls, query: dict, collection, excluded_fields: Optional[dict] = None):
        collections = cls.db[f'{collection}']
        cursor = collections.find(query, excluded_fields)
        return cursor

    @classmethod
    async def delete(cls, query: dict, collection):
        collections = cls.db[f'{collection}']
        collections.delete_many(query)
