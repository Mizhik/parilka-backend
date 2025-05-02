from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.hookahs import HookahsRepository
from app.schemas.filters import ProductFilterParams
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class HookahsService:
    def __init__(self, db: AsyncSession, repository: HookahsRepository):
        self.db = db
        self.repository = repository

    async def get_hookahs(self, filters: ProductFilterParams):
        hookahs = await self.repository.get_hookahs(
            offset=filters.offset,
            limit=filters.limit,
            min_price=filters.min_price,
            max_price=filters.max_price,
            manufacturer_ids=filters.manufacturer_id,
        )
        hookahs_schema = [map_product_to_schema(hookah) for hookah in hookahs]
        return ResponseSchema(data=hookahs_schema, message="All hookahs.")
