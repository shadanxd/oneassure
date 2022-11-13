from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.environ.get('username')
db_password = os.environ.get('password')
cluster = MongoClient(f'mongodb+srv://{db_user}:{db_password}@cluster0.ef68wuq.mongodb.net/?retryWrites=true&w=majority')
db = cluster["Cluster0"]
collections = db["test"]


class Data:
    def __init__(self, username: str):
        self.username = username

    @classmethod
    def save(cls, item: dict):
        collections.insert_one(item)
        return cls(item['_id'])

    def user_query(self):
        results = collections.find_one({"_id": self.username})
        if results:
            return results['password']
        else:
            return None

    def update_phone(self, phone: int):
        collections.update_one({"_id": self.username}, {"$set": {"phone": phone}})

    def name_update(self, new_name: str):
        collections.update_one({"_id": self.username}, {"$set": {"name": new_name}})

    def getUserDetails(self):
        user = collections.find_one({"_id": self.username})
        return user



