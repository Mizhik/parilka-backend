from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select, update
from app.models.models import Category
from app.repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db):
        super().__init__(db=db, model=Category)

    async def get_by_title(self, title: str) -> Optional[Category]:
        stmt = select(self.model).where(self.model.title == title)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update(self, category_id: UUID, values: dict):
        stmt = update(self.model).where(self.model.id==category_id).values(**values).returning(self.model)
        result = await self.db.execute(stmt)
        updated_category = result.scalars().first()
        if updated_category:
            await self.db.commit()
        return updated_category
    
    async def delete(self, category_id: UUID):
        stmt = delete(self.model).where(self.model.id==category_id).returning(self.model)
        result = await self.db.execute(stmt)
        deleted_category = result.scalars().first()
        if deleted_category:
            await self.db.commit()
