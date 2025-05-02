from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.components import ComponentsRepository
from app.schemas.filters import ProductFilterParams
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class ComponentsService:
    def __init__(self, db: AsyncSession, repository: ComponentsRepository):
        self.db = db
        self.repository = repository

    async def get_components(self, filters: ProductFilterParams):
        components = await self.repository.get_components(
            offset=filters.offset,
            limit=filters.limit,
            min_price=filters.min_price,
            max_price=filters.max_price,
            manufacturer_ids=filters.manufacturer_id,
        )
        components_schema = [map_product_to_schema(component) for component in components]
        return ResponseSchema(data=components_schema, message="All components products")
