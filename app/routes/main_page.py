from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.schemas.main_page import MainPageSchema
from app.schemas.response import ResponseSchema
from app.services.dependencies import get_main_page_service
from app.services.main_page import MainPageService


router = APIRouter(prefix="/main-page", tags=["Main page"])


@router.get("", response_model=ResponseSchema[MainPageSchema])
@cache(expire=60 * 8)
async def get_main_page(service: MainPageService = Depends(get_main_page_service)):
    return await service.get_main_page()
