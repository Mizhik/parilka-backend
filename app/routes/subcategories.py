
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from app.schemas.response import ResponseSchema
from app.schemas.subcategory import CreateSubCategorySchema, EditSubCategorySchema, SubCategorySchema
from app.services.dependencies import get_subcategory_service
from app.services.subcategory import SubCategoryService


router = APIRouter(prefix="/subcategories", tags=["Sub-categories"])

@router.get("", response_model=ResponseSchema[List[SubCategorySchema]])
async def get_all(service: SubCategoryService = Depends(get_subcategory_service)):
    return await service.get_all()

@router.post("/add", response_model=ResponseSchema[SubCategorySchema])
async def add_subcategory(body: CreateSubCategorySchema, service: SubCategoryService = Depends(get_subcategory_service)):
    return await service.create(body)

@router.patch("/edit/{subcategory_id}", response_model=ResponseSchema[SubCategorySchema])
async def edit_subcategory(subcategory_id: UUID, body: EditSubCategorySchema, service: SubCategoryService = Depends(get_subcategory_service)):
    return await service.edit(subcategory_id, body)

@router.delete("/delete/{subcategory_id}", response_model=ResponseSchema)
async def delete_subcategory(subcategory_id: UUID, service: SubCategoryService = Depends(get_subcategory_service)):
    return await service.delete(subcategory_id)
