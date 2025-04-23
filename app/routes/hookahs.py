from fastapi import APIRouter, Depends
from typing import List, Optional

from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.hookahs import HookahsService
from app.services.dependencies import get_hookahs_service


router = APIRouter(prefix="/hookahs", tags=["Hookahs"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_hookahs(
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        hookahs_service: HookahsService = Depends(get_hookahs_service)
):
    return await hookahs_service.get_hookahs(offset=offset, limit=limit)