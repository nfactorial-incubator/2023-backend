from app.config import database

from .repository.repository import ShanyrakRepository
from .adapters.s3_service import S3Service
from .repository.comments_repository import CommentRepository

class Service:
    def __init__(self):
        self.repository = ShanyrakRepository(database)
        self.comment_repository = CommentRepository(database)
        self.s3_service = S3Service()


def get_service():
    return Service()
