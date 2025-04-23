from fastapi import APIRouter, Depends
from typing import List, Optional

from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.components import ComponentsService
from app.services.dependencies import get_components_service


router = APIRouter(prefix="/components", tags=["Components"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_components(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    components_service: ComponentsService = Depends(get_components_service)
):
    return await components_service.get_components(offset=offset, limit=limit)
