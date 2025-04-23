from fastapi import APIRouter, Depends
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
    liquids_service: LiquidsService = Depends(get_liquids_service)
):
    return await liquids_service.get_liquids(offset=offset, limit=limit)
