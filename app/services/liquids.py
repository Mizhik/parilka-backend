from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.liquids import LiquidsRepository
from app.schemas.response import ResponseSchema
from app.schemas.filters import ProductFilterParams
from app.utils.mappers import map_product_to_schema


class LiquidsService:
    def __init__(self, db: AsyncSession, repository: LiquidsRepository):
        self.db = db
        self.repository = repository

    async def get_liquids(self, filters: ProductFilterParams):
        liquids = await self.repository.get_liquids(
            offset=filters.offset,
            limit=filters.limit,
            min_price=filters.min_price,
            max_price=filters.max_price,
            manufacturer_ids=filters.manufacturer_id
        )
        liquids_schema = [map_product_to_schema(liquid) for liquid in liquids]
        return ResponseSchema(data=liquids_schema, message="All liquids products")
