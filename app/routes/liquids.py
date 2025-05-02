from fastapi import APIRouter, Depends, Query
from typing import List

from typing_extensions import Annotated

from app.schemas.filters import ProductFilterParams
from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.dependencies import get_liquids_service
from app.services.liquids import LiquidsService


router = APIRouter(prefix="/liquids", tags=["Liquids"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_liquids(
    filters: Annotated[ProductFilterParams, Query()],
    liquids_service: LiquidsService = Depends(get_liquids_service)
):
    return await liquids_service.get_liquids(**filters.dict(exclude_none=True))
