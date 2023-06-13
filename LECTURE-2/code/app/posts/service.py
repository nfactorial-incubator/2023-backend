from app.config import database

from .repository.repository import PostRepository


class Service:
    def __init__(self):
        self.repository = PostRepository(database)


def get_service():
    svc = Service()
    return svc
