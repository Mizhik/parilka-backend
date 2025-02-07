from app.models.models import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=User)
