from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List

from fastapi.responses import JSONResponse

from app.schemas.category import CategorySchema
from app.schemas.response import ResponseSchema
from app.services.category import CategoryService
from app.services.dependencies import get_category_service
from app.services.errors import DuplicateError

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=ResponseSchema[List[CategorySchema]])
async def get_categories(category_service: CategoryService = Depends(get_category_service)):
    return await category_service.get_all()

@router.post("/add", response_model=ResponseSchema[CategorySchema])
async def create_category(body: CategorySchema, category_service: CategoryService = Depends(get_category_service)):
    try:
        return await category_service.create(body)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
