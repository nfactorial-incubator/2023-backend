from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, payload: dict):
        payload["user_id"] = ObjectId(user_id)
        shanyrak = self.database["shanyraks"].insert_one(payload)
        return shanyrak.inserted_id

    def get_shanyrak_by_id(self, shanyrak_id: str, user_id: str) -> Optional[dict]:
        user = self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return user

    def get_all_shanyraks(self, user_id: str) -> List[dict]:
        shanyraks = self.database["shanyraks"].find({"user_id": ObjectId(user_id)})
        return list(shanyraks)
    
    def update_shanyrak_by_id(self, shanyrak_id: str, user_id: str, data: dict) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak_by_id(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
