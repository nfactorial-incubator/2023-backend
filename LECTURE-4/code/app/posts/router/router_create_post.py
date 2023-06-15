from fastapi import Depends, Response

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    address: str


@router.post("/")
def create_post(
    inpu: CreatePostRequest,
    svc: Service = Depends(get_service),
):
    
    result = svc.here_service.get_coordinates(inpu.address)

    return result
