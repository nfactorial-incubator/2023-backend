from datetime import datetime
from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetCommentResponse(AppModel):
    id: Any = Field(alias="_id")
    content: str
    created_at: str
    author_id: str
@router.get("/{id:str}/comments", response_model=List[GetCommentResponse])
def get_shanyrak(
        id: str,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
) -> List[GetCommentResponse]:
    comments = svc.comment_repository.get_comments_by_shanyrak_id(shanyrak_id=id)
    return [GetCommentResponse(**comment) for comment in comments]
