from typing import Dict, List
from fastapi import APIRouter, Depends

from app.models.enums import ConstructorTag
from app.schemas.constructor import ConstructorComponent, ConstructorSchema
from app.schemas.response import ResponseSchema
from app.services.constructor import ConstructorService
from app.services.dependencies import get_constructor_service

router = APIRouter(prefix="/constructor", tags=["Constructor"])

@router.get("", response_model=ResponseSchema[Dict[ConstructorTag, ConstructorSchema]])
async def get_all(constructor_service: ConstructorService = Depends(get_constructor_service)):
    return await constructor_service.get_all()

@router.get("/{constructor_tag}", response_model=ResponseSchema[List[ConstructorComponent]])
async def get_constructor(constructor_tag: ConstructorTag, constructor_service: ConstructorService = Depends(get_constructor_service)):
    return await constructor_service.get_by_tag(constructor_tag)

@router.patch("/edit/{constructor_tag}", response_model=ResponseSchema[ConstructorSchema])
async def change_constructor_components_by_tag(
        constructor_tag: ConstructorTag,
        body: List[ConstructorComponent],
        constructor_service: ConstructorService = Depends(get_constructor_service)
):
    return await constructor_service.edit(constructor_tag, body)
