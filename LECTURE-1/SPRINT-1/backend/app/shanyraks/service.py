from app.config import database

from .repository.repository import ShanyrakRepository


class Service:
    def __init__(
        self,
        repository: ShanyrakRepository,
    ):
        self.repository = repository


def get_service():
    repository = ShanyrakRepository(database)
    return Service(repository)
