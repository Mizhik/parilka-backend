from typing import Any, Dict, List
from sqlalchemy import update
from app.models.enums import ConstructorTag
from app.models.models import Constructor
from app.repository.base_repository import BaseRepository


class ConstructorRepository(BaseRepository[Constructor]):
    def __init__(self, db):
        super().__init__(db=db, model=Constructor)

    async def update(self, body: Any, **params) -> Constructor | None:
        return await super().update({"component_data": body}, **params)
