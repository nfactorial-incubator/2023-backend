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

    def get_posts(
            self,
            limit: int,
            offset: int,
            type: Optional[str] = None,
            rooms_count: Optional[int] = None,
            price_from: Optional[int] = None,
            price_to: Optional[int] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            radius: Optional[int] = None,
    ):
        filter_criteria = {}

        if price_from is not None and price_to is not None:
            filter_criteria["price"] = {
                "$gte": price_from,
                "$lte": price_to
            }
        if type is not None:
            filter_criteria["type"] = type
        if rooms_count is not None:
            filter_criteria["rooms_count"] = rooms_count
        if latitude is not None and longitude is not None and radius is not None:
            radians = radius / 6371.0
            filter_criteria["location"] = {
                "$geoWithin": {
                    "$centerSphere": [[longitude, latitude], radians]
                }
            }

        total = self.database["shanyraks"].count_documents(filter_criteria)
        cursor = self.database["shanyraks"] \
            .find(filter_criteria).limit(limit).skip(offset).sort("created_at")

        result = []
        for document in cursor:
            result.append(document)

        return {
            "total": total,
            "objects": result
        }
