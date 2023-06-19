from pydantic import BaseSettings

from app.config import database

from .adapters.here_service import HereService
from .adapters.s3_service import S3Service
from .repository.comments_repository import CommentRepository
from .repository.repository import ShanyrakRepository


class Config(BaseSettings):
    HERE_API_KEY: str


class Service:
    def __init__(self):
        config = Config()
        self.repository = ShanyrakRepository(database)
        self.comment_repository = CommentRepository(database)
        self.s3_service = S3Service()
        self.here_service = HereService(config.HERE_API_KEY)


def get_service():
    return Service()
