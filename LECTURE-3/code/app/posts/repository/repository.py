# from datetime import datetime
# from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, input: dict):
        payload = {
            "city": input["city"],
            "message": input["message"],
            "user_id": ObjectId(input["user_id"])
        }

        self.database["posts"].insert_one(payload)
