from typing import Optional
from sqlalchemy import select
from app.models.models import Category
from app.repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db):
        super().__init__(db=db, model=Category)

    async def get_by_title(self, title: str) -> Optional[Category]:
        stmt = select(self.model).where(self.model.title == title)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
