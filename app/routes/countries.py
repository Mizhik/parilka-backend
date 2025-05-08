from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from app.schemas.country import CountryCreateSchema, CountrySchema
from app.schemas.response import ResponseSchema
from app.services.country import CountryService
from app.services.dependencies import get_country_service


router = APIRouter(prefix="/countries", tags=["Countries"])

@router.get("", response_model=ResponseSchema[List[CountrySchema]])
async def get_all(service: CountryService = Depends(get_country_service)):
    return await service.get_all()

@router.post("/add", response_model=ResponseSchema[CountrySchema])
async def create_country(body: CountryCreateSchema, service: CountryService = Depends(get_country_service)):
    return await service.create(body)

@router.patch("/edit/{country_id}", response_model=ResponseSchema[CountrySchema])
async def edit_country(country_id: UUID, body: CountryCreateSchema, service: CountryService = Depends(get_country_service)):
    return await service.edit(country_id, body)

@router.delete("/delete/{country_id}", response_model=ResponseSchema)
async def delete_country(country_id: UUID, service: CountryService = Depends(get_country_service)):
    return await service.delete(country_id)
