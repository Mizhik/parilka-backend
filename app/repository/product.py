from typing import Optional

from sqlalchemy.future import select

from app.models.models import Product
from app.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Product)

    async def get_popular(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ):
        stmt = select(self.model).where(self.model.is_popular.is_(True))
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

