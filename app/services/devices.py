from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.devices import DevicesRepository
from app.schemas.response import ResponseSchema
from app.schemas.filters import ProductFilterParams
from app.utils.mappers import map_product_to_schema


class DevicesService:
    def __init__(self, db: AsyncSession, repository: DevicesRepository):
        self.db = db
        self.repository = repository

    async def get_devices(self, filters: ProductFilterParams):
        devices = await self.repository.get_devices(
            offset=filters.offset,
            limit=filters.limit,
            min_price=filters.min_price,
            max_price=filters.max_price,
            manufacturer_ids=filters.manufacturer_ids,
        )
        devices_schema = [map_product_to_schema(device) for device in devices]
        return ResponseSchema(data=devices_schema, message="All devices products")
