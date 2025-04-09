from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.models import Product
from app.repository.base_repository import BaseRepository, ModelType


class ProductRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Product)

    async def get_popular(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ):
        stmt = (select(self.model)
                .where(self.model.is_popular.is_(True))
                .options(selectinload(self.model.images), selectinload(self.model.attributes))
                )
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_many(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[ModelType]:
        stmt = select(self.model).options(
            selectinload(self.model.images),
            selectinload(self.model.attributes)
        )

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, product_id: UUID, values: dict):
        stmt = update(self.model).where(self.model.id==product_id).values(**values).returning(self.model)
        result = await self.db.execute(stmt)
        updated_product = result.scalars().first()
        if updated_product:
            await self.db.commit()
        return updated_product

    async def delete(self, product_id: UUID):
        stmt = delete(self.model).where(self.model.id==product_id).returning(self.model)
        result = await self.db.execute(stmt)
        deleted_product = result.scalars().first()
        if deleted_product:
            await self.db.commit()
            return deleted_product
        return None
