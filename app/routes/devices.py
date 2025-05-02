from fastapi import APIRouter, Depends, Query
from typing import List

from typing_extensions import Annotated

from app.schemas.filters import ProductFilterParams
from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.devices import DevicesService
from app.services.dependencies import get_devices_service

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_devices(
    filters: Annotated[ProductFilterParams, Query()],
    devices_service: DevicesService = Depends(get_devices_service)
):
    return await devices_service.get_devices(**filters.dict(exclude_none=True))
