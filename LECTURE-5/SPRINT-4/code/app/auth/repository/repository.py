from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def delete_user_like(self, user_id: str, shanyrak_id: str):
        likes = self.get_user_likes(user_id)
        print(likes)
        if shanyrak_id in likes:
            likes.remove(shanyrak_id)

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": likes,
                }
            },
        )

    def set_user_like(self, user_id: str, shanyrak_id: str):
        likes = self.get_user_likes(user_id)
        print(likes)
        if shanyrak_id not in likes:
            likes.append(shanyrak_id)

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": likes,
                }
            },
        )

    def get_user_likes(self, user_id: str) -> list:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user["likes"] if "likes" in user else []

    def get_shanyraks_by_id(self, user_id) -> list:
        shanyrak_ids = self.get_user_likes(user_id)
        obj_shanyrak_ids = [ObjectId(shanyrak_id) for shanyrak_id in shanyrak_ids]
        print("ids", obj_shanyrak_ids)
        shanyraks = self.database["shanyraks"].find({"_id": {"$in": obj_shanyrak_ids}})

        return list(shanyraks)

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def save_avatar(self, user_id: str, url: str):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "avatar_url": 1,
                }
            },
        )

    def delete_avatar(self, user_id: str):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$unset": {
                    "avatar_url": "",
                }
            },
        )

    def like_shanyrak(self, user_id: str, shanyrak_id: str):
        likes = self.find_likes(user_id)
        if shanyrak_id not in likes:
            likes.append(shanyrak_id)
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": likes,
                }
            },
        )

    def get_shanyraks(self, shanyrak_ids: list):
        ids = [ObjectId(id) for id in shanyrak_ids]
        shanyraks = self.database["shanyraks"].find({"_id": {"$in": ids}}, {"_id": 1, "address": 1})
        return [shanyrak for shanyrak in shanyraks]

    def get_all_likes(self, user_id: str):
        likes = self.find_likes(user_id)
        return self.get_shanyraks(likes)

    def delete_liked_shanyrak(self, user_id: str, shanyrak_id: str):
        likes = self.find_likes(user_id)
        if shanyrak_id in likes:
            likes.remove(shanyrak_id)
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": likes,
                }
            },
        )

    def find_likes(self, user_id: str) -> list:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        print(user)
        return user["likes"] if "likes" in user else []
