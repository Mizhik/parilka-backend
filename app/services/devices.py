from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.devices import DevicesRepository
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class DevicesService:
    def __init__(self, db: AsyncSession, repository: DevicesRepository):
        self.db = db
        self.repository = repository

    async def get_devices(self, offset: Optional[int] = None, limit: Optional[int] = None):
        devices = await self.repository.get_devices(offset=offset, limit=limit)
        devices_schema = [map_product_to_schema(device) for device in devices]
        return ResponseSchema(data=devices_schema, message="All devices products")
