from typing import Any, List

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetMyTweetsTweet(AppModel):
    id: Any = Field(alias="_id")
    content: str


class GetMyTweetsResponse(AppModel):
    tweets: List[GetMyTweetsTweet]


@router.get("/", response_model=GetMyTweetsResponse)
def get_my_tweets(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    tweets = svc.repository.get_tweet_by_user_id(user_id)

    resp = {"tweets": tweets}

    return resp
