from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.dependencies import get_liquids_service
from app.services.liquids import LiquidsService


router = APIRouter(prefix="/liquids", tags=["Liquids"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_liquids(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    manufacturer_ids: Optional[List[int]] = Query(default=None),
    liquids_service: LiquidsService = Depends(get_liquids_service)
):
    filters = {
        "min_price": min_price,
        "max_price": max_price,
        "manufacturer_ids": manufacturer_ids,
    }
    return await liquids_service.get_liquids(offset=offset, limit=limit, **filters)
