from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database


class TweetRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_tweet(self, input: dict):
        payload = {
            "content": input["content"],
            "user_id": ObjectId(input["user_id"]),
            "created_at": datetime.utcnow(),
        }

        self.database["tweets"].insert_one(payload)

    def get_tweet_by_user_id(self, user_id: str) -> List[dict]:
        tweets = self.database["tweets"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []
        for tweet in tweets:
            result.append(tweet)

        return result
