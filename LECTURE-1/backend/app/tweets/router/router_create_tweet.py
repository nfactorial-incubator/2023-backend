from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateTweetRequest(AppModel):
    content: str


@router.post("/")
def create_tweet(
    input: CreateTweetRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    svc.repository.create_tweet({"user_id": user_id, "content": input.content})

    return Response(status_code=200)
