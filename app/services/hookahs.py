from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.hookahs import HookahsRepository
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class HookahsService:
    def __init__(self, db: AsyncSession, repository: HookahsRepository):
        self.db = db
        self.repository = repository

    async def get_hookahs(self, offset: Optional[int] = None, limit: Optional[int] = None):
        hookahs = await self.repository.get_hookahs(offset=offset, limit=limit)
        hookahs_shema = [map_product_to_schema(hookah) for hookah in hookahs]
        return ResponseSchema(data=hookahs_shema, message="All hookahs.")
