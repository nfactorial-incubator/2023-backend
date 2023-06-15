from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult

class CommentRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_comment(self, shanyrak_id: str, user_id: str, payload: dict):
        payload["shanyrak_id"] = ObjectId(shanyrak_id)
        payload["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload["author_id"] = user_id
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        if not shanyrak:
            raise HTTPException(status_code=404, detail=f"Could find shanyrak with id {shanyrak_id}")
        payload["user_id"] = ObjectId(user_id)
        comment = self.database["comments"].insert_one(payload)
        return comment.acknowledged

    def get_comments_by_shanyrak_id(self, shanyrak_id: str) -> List[dict]:
        comments = self.database["comments"].find({"shanyrak_id": ObjectId(shanyrak_id)})
        return list(comments)

    def update_comment_by_id(self, comment_id: str, user_id: str, data: dict) -> UpdateResult:
        return self.database["comments"].update_one(
            filter={"_id": ObjectId(comment_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_comment_by_id(self, comment_id: str, user_id: str) -> DeleteResult:
        return self.database["comments"].delete_one(
            {"_id": ObjectId(comment_id), "user_id": ObjectId(user_id)}
        )
