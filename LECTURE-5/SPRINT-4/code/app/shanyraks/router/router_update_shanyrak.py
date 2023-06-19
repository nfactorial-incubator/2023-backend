from typing import Any, List
import imghdr

from fastapi import Depends, Response, HTTPException, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id:str}")
def update_shanyrak(
    shanyrak_id: str,
    input: UpdateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    update_result = svc.repository.update_shanyrak_by_id(
        shanyrak_id=shanyrak_id, user_id=jwt_data.user_id, data=input.dict()
    )
    if update_result.modified_count == 1:
        return Response(status_code=200)
    raise HTTPException(status_code=404, detail=f"Shanyrak {shanyrak_id} not found")


@router.post("/{shanyrak_id:str}/media")
def update_shanyrak_photos(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    media_urls = []
    for file in files:
        if not is_image(file.file.read()):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not image")
        url = svc.s3_service.upload_file(file.file, file.filename)
        if url is None:
            raise HTTPException(status_code=500, detail=f"File {file.filename} not uploaded")
        media_urls.append(url)
    update_result = svc.repository.update_shanyrak_by_id(
        shanyrak_id=shanyrak_id, user_id=jwt_data.user_id, data={"media": media_urls}
    )
    if update_result.acknowledged:
        return media_urls
    raise HTTPException(status_code=404, detail=f"Error occured while updating shanyrak {shanyrak_id}")


@router.delete("/{shanyrak_id:str}/media")
def delete_shanyrak_photos(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    shanyrak = svc.repository.get_shanyrak_by_id(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id)
    to_delete = shanyrak.get("media", [])
    for url in to_delete:
        svc.s3_service.delete_file(url.split("/")[-1])
    update_result = svc.repository.update_shanyrak_by_id(
        shanyrak_id=shanyrak_id, user_id=jwt_data.user_id, data={"media": []}
    )
    if not update_result.acknowledged:
        raise HTTPException(status_code=404, detail=f"Error occured while deleting photos from shanyrak {shanyrak_id}")
    return to_delete


def is_image(file_contents: bytes) -> bool:
    image_type = imghdr.what(None, file_contents)
    return image_type is not None
