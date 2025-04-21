from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.models.models import Product
from app.repository.base_repository import BaseRepository, ModelType


class ProductRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db,
                         model=Product,
                         lazyopts=[selectinload(Product.images), selectinload(Product.attributes)]
                        )


    async def get_popular(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ):
        stmt = (select(self.model)
                .where(self.model.is_popular.is_(True))
                .options(*self.lazyopts)
                )
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_with_relations_by_id(self, obj_id: UUID) -> ModelType:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.images),
                selectinload(self.model.attributes),
            )
            .where(self.model.id == obj_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, product_id: UUID, values: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == product_id)
            .values(**values)
        )
        await self.db.execute(stmt)
        await self.db.commit()

        updated_product = await self.get_with_relations_by_id(product_id)
        return updated_product

    async def delete(self, product_id: UUID):
        stmt = delete(self.model).where(self.model.id==product_id).returning(self.model)
        result = await self.db.execute(stmt)
        deleted_product = result.scalars().first()
        if deleted_product:
            await self.db.commit()
            return deleted_product
        return None
