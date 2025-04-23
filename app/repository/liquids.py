from typing import Optional, List

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.models import Product, Category
from app.repository.base_repository import BaseRepository


class LiquidsRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(db=db,
                         model=Product,
                         lazyopts=[selectinload(Product.images), selectinload(Product.attributes)]
                         )

    async def get_liquids(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            manufacturer_ids: Optional[List[int]] = None,
    ) -> List[Product]:
        stmt = (
            select(self.model)
            .join(self.model.category)
            .join(self.model.manufacturer)
            .where(Category.title.ilike("liquid"))
        )

        filters = []

        if min_price is not None:
            filters.append(Product.price >= min_price)
        if max_price is not None:
            filters.append(Product.price <= max_price)
        if manufacturer_ids:
            filters.append(Product.manufacturer_id.in_(manufacturer_ids))

        if filters:
            stmt = stmt.where(and_(*filters))

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()
