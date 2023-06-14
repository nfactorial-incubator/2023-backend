from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    city: str
    message: str

@router.post("/")
def create_post(
    inpu: CreatePostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    payload = inpu.dict()
    payload["user_id"] = jwt_data.user_id
    
    svc.repository.create_post(payload)
    
    return Response(status_code=200)
