from datetime import datetime

# from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database


class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, input: dict):
        payload = {
            "address": input["address"],
            "price": input["price"],
            "type": input["type"],
            "rooms_count": input["rooms_count"],
            "created_at": datetime.utcnow(),
        }

        self.database["posts"].insert_one(payload)

    def get_posts(self, limit: int, offset: int, rooms_count):
        total_count = self.database["posts"].count_documents({
            "rooms_count": {
                "$gt": rooms_count
            },
        })
        
        cursor = self.database["posts"].find({
            "rooms_count": {
                "$gt": rooms_count
            },
        }).limit(limit).skip(offset).sort("created_at")
        
        result = []
        for item in cursor:
            result.append(item)
        
        return {
            "total": total_count,
            "objects": result
        }
        
