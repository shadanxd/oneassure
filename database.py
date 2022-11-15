#new line
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.environ.get('username')
db_password = os.environ.get('password')
cluster = MongoClient(f'mongodb+srv://{db_user}:{db_password}@cluster0.ef68wuq.mongodb.net/?retryWrites=true&w=majority')
db = cluster["Cluster0"]
collections = db["OneAssure"]


class DBHandler:
    def __init__(self, username: str):
        self.username = username

    @classmethod
    async def save(cls, item: dict):
        collections.insert_one(item)
        return cls(item['_id'])

    async def user_query(self):
        results = collections.find_one({"_id": self.username})
        if results:
            return results['password']
        else:
            return None

    async def update_phone(self, phone: int):
        collections.update_one({"_id": self.username}, {"$set": {"phone": phone}})

    async def name_update(self, new_name: str):
        collections.update_one({"_id": self.username}, {"$set": {"name": new_name}})

    async def getUserDetails(self):
        user = collections.find_one({"_id": self.username})
        return user



