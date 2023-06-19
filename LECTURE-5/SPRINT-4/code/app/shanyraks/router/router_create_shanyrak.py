from typing import Any, List, Optional

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Location(AppModel):
    type: str = 'Point'
    coordinates: List[float]


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



class Shanyrak(AppModel):
    address: str
    price: int
    type: str
    rooms_count: int
    location: Location

class GetShanyrakResponse(AppModel):
    total: int
    objects: List[Shanyrak]

@router.post("/asdasd")
def asdasd():
    return "asdasd"

@router.get("/asda", response_model=GetShanyrakResponse)
def get_posts(
    limit: int = 10,
    offset: int = 0,
    type: Optional[str] = None,
    rooms_count: Optional[int] = None,
    price_from: Optional[int] = None,
    price_to: Optional[int] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = None,
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_posts(
        limit,
        offset,
        type,
        rooms_count,
        price_from,
        price_to,
        latitude,
        longitude,
        radius
    )
    return result