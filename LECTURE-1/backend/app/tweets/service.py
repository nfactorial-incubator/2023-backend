from app.config import database

from .repository.repository import TweetRepository


class Service:
    def __init__(
        self,
        repository: TweetRepository,
    ):
        self.repository = repository


def get_service():
    repository = TweetRepository(database)

    svc = Service(repository)
    return svc
