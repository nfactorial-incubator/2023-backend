from typing import Any

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Location(AppModel):
    latitude: float
    longitude: float


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post("/", response_model=CreateShanyrakResponse)
def create_shanyrak(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    print(input.dict())
    save_data = input.dict() | svc.here_service.get_coordinates(input.address)
    print(save_data)
    inserted_id = svc.repository.create_shanyrak(user_id=user_id, payload=save_data)
    return CreateShanyrakResponse(id=inserted_id)
