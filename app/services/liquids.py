from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.liquids import LiquidsRepository
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class LiquidsService:
    def __init__(self, db: AsyncSession, repository: LiquidsRepository):
        self.db = db
        self.repository = repository

    async def get_liquids(self, offset: Optional[int] = None, limit: Optional[int] = None, **filters):
        products = await self.repository.get_liquids(offset=offset, limit=limit, **filters)
        products_schema = [map_product_to_schema(product) for product in products]
        return ResponseSchema(data=products_schema, message="All liquids products")
