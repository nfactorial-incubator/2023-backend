from typing import Any, List

from fastapi import Depends, Response, status
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Shanyrak(AppModel):
    id: Any = Field(alias="_id")
    address: str


class ShanyrakLikes(AppModel):
    shanyraks: List[Shanyrak]


@router.post(
    "/users/favorites/shanyraks/{shanyrak_id:str}",
    status_code=status.HTTP_200_OK,
)
def like_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    svc.repository.like_shanyrak(jwt_data.user_id, shanyrak_id)
    return Response(status_code=200)


@router.delete(
    "/users/favorites/shanyraks/{shanyrak_id:str}",
    status_code=status.HTTP_200_OK,
)
def delete_like_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    svc.repository.delete_liked_shanyrak(jwt_data.user_id, shanyrak_id)
    return Response(status_code=200)


@router.get(
    "/auth/users/favorites/shanyraks",
    response_model=ShanyrakLikes,
    status_code=status.HTTP_200_OK,
)
def get_liked_shanyraks(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    shanyraks = svc.repository.get_all_likes(jwt_data.user_id)
    return ShanyrakLikes(shanyraks=shanyraks)
