from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload

from app.models.models import Product, Category
from app.repository.base_repository import BaseRepository
from app.repository.product_filters import product_filters


class DevicesRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(db=db,
                         model=Product,
                         lazyopts=[selectinload(Product.images), selectinload(Product.attributes)]
                         )

    async def get_devices(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            manufacturer_ids: Optional[List[UUID]] = None,
    ) -> List[Product]:
        stmt = (
            select(self.model)
            .distinct()
            .join(Category)
            .where(Category.title.ilike("device"))
        )

        filters = product_filters(min_price, max_price, manufacturer_ids)

        if filters:
            stmt = stmt.where(and_(*filters))

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()
