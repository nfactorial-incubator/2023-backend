from typing import List, Optional

from fastapi import Depends, Response

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    address: str
    price: int
    type: str
    rooms_count: int


@router.post("/")
def create_post(
    input: CreatePostRequest,
    svc: Service = Depends(get_service),
):
    payload = input.dict()
    svc.repository.create_post(payload)

    return Response(status_code=200)


class Post(AppModel):
    address: str
    price: int
    type: str
    rooms_count: int


class GetPostsResponse(AppModel):
    total: int
    objects: List[Post]
    

@router.get("/", response_model=GetPostsResponse)
def get_posts(
    limit: int,
    offset: int,
    rooms_count: Optional[int] = None,
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_posts(limit, offset, rooms_count)
    return result


