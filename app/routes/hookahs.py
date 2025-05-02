from fastapi import APIRouter, Depends, Query
from typing import List

from typing_extensions import Annotated

from app.schemas.filters import ProductFilterParams
from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.hookahs import HookahsService
from app.services.dependencies import get_hookahs_service

router = APIRouter(prefix="/hookahs", tags=["Hookahs"])


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
async def get_hookahs(
       filters: Annotated[ProductFilterParams, Query()],
        hookahs_service: HookahsService = Depends(get_hookahs_service)
):
    return await hookahs_service.get_hookahs(**filters.dict(exclude_none=True))
