from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select, update
from app.models.models import Category, Constructor
from app.repository.base_repository import BaseRepository


class ConstructorRepository(BaseRepository[Constructor]):
    def __init__(self, db):
        super().__init__(db=db, model=Constructor)

