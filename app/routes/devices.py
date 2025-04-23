from fastapi import APIRouter, Depends
from typing import List, Optional

from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.devices import DevicesService
from app.services.dependencies import get_devices_service

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_devices(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    devices_service: DevicesService = Depends(get_devices_service)
):
    return await devices_service.get_devices(offset=offset, limit=limit)
