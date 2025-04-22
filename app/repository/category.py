from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select, update
from app.models.models import Category
from app.repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db):
        super().__init__(db=db, model=Category)
