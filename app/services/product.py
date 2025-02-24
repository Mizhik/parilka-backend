from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.product import ProductRepository


class ProductService:
    def __init__(self, db: AsyncSession, repository: ProductRepository):
        self.db = db
        self.repository = repository

    async def get_popular_products(self, offset: Optional[int] = None, limit: Optional[int] = None):
        return await self.repository.get_popular(offset, limit)
