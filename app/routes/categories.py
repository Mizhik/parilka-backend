from uuid import UUID
from fastapi import APIRouter, Body, Depends
from typing import List


from app.schemas.category import CategorySchema
from app.schemas.response import ResponseSchema
from app.services.category import CategoryService
from app.services.dependencies import get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=ResponseSchema[List[CategorySchema]])
async def get_categories(
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get_all()


@router.post("/add", response_model=ResponseSchema[CategorySchema])
async def create_category(
    body: CategorySchema = Body(
        ..., examples=[CategorySchema(id=None, title="string")]
    ),
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.create(body)


@router.patch("/edit/{category_id}", response_model=ResponseSchema[CategorySchema])
async def edit_category(
    category_id: UUID,
    body: CategorySchema = Body(
        ..., examples=[CategorySchema(id=None, title="string")]
    ),
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.edit(category_id, body)


@router.delete("/delete/{category_id}", response_model=ResponseSchema)
async def delete_category(
    category_id: UUID, category_service: CategoryService = Depends(get_category_service)
):
    return await category_service.delete(category_id)
