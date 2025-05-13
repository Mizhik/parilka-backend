from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from typing_extensions import Annotated

from app.schemas.filters import ProductFilterParams
from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.components import ComponentsService
from app.services.dependencies import get_components_service

router = APIRouter(prefix="/components", tags=["Components"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_components(
    filters: Annotated[ProductFilterParams, Query()],
    components_service: ComponentsService = Depends(get_components_service)
):
    return await components_service.get_components(filters)
