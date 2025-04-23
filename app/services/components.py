from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.components import ComponentsRepository
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class ComponentsService:
    def __init__(self, db: AsyncSession, repository: ComponentsRepository):
        self.db = db
        self.repository = repository

    async def get_components(self, offset: Optional[int] = None, limit: Optional[int] = None):
        components = await self.repository.get_components(offset=offset, limit=limit)
        components_schema = [map_product_to_schema(component) for component in components]
        return ResponseSchema(data=components_schema, message="All components products")
