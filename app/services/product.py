from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repository.product import ProductRepository
from app.schemas.product import ProductBase, ProductCreate, ProductResponse
from app.services.errors import ErrorNotFound


class ProductService:
    def __init__(self, db: AsyncSession, repository: ProductRepository):
        self.db = db
        self.repository = repository

    async def get_popular_products(self, offset: Optional[int] = None, limit: Optional[int] = None):
        return await self.repository.get_popular(offset, limit)

    async def get_all_product(self, offset: Optional[int] = None, limit: Optional[int] = None):
        return await self.repository.get_many(offset, limit)

    async def get_one_product(self, product_id: UUID):
        product = await self.repository.get_one(id=product_id)
        if not product:
            raise ErrorNotFound(f"Продукт з ID: {product_id} не знайдено.")

        return product

    async def create_product(self, body: ProductCreate):
        values = body.dict(exclude_unset=True)
        created_product = await self.repository.create(values)
        return created_product

    async def edit_product(self, product_id: UUID, body: ProductBase):
        values = body.dict(exclude_unset=True)
        updated_product = await self.repository.update(product_id, values)
        if not updated_product:
            raise ErrorNotFound(f"Продукт з ID: {product_id} не знайдено.")

        return updated_product

    async def delete_product(self, product_id: UUID):
        deleted_product = await self.repository.delete(product_id)
        if not deleted_product:
            raise ErrorNotFound(f"Продукт з ID: {product_id} не знайдено.")

        return deleted_product
