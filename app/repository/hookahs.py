from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.models import Product, Category
from app.repository.base_repository import BaseRepository


class HookahsRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(db=db,
                         model=Product,
                         lazyopts=[selectinload(Product.images), selectinload(Product.attributes)]
                         )

    async def get_hookahs(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            **params
    ) -> List[Product]:
        stmt = select(self.model).join(Category).where(Category.title.ilike("hookah"))

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()
