from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from app.schemas import response
from app.schemas.manufacturer import ManufacturerCreateSchema, ManufacturerSchema
from app.schemas.response import ResponseSchema
from app.services.dependencies import get_manufacturer_service
from app.services.manufacturer import ManufacturerService

router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])

@router.get("", response_model=ResponseSchema[List[ManufacturerSchema]])
async def get_manufacturers(service: ManufacturerService = Depends(get_manufacturer_service)):
    return await service.get_all()

@router.post("/add", response_model=ResponseSchema[ManufacturerSchema])
async def create_manufacturer(
    body: ManufacturerCreateSchema,
    service: ManufacturerService = Depends(get_manufacturer_service)
):
    return await service.create(body)

@router.patch("/edit/{manufacturer_id}", response_model=ResponseSchema[ManufacturerSchema])
async def edit_manufacturer(manufacturer_id: UUID, body: ManufacturerCreateSchema, service: ManufacturerService = Depends(get_manufacturer_service)):
    return await service.edit(manufacturer_id, body)

@router.delete("/delete/{manufacturer_id}", response_model=ResponseSchema)
async def delete_manufacturer(manufacturer_id: UUID, service: ManufacturerService = Depends(get_manufacturer_service)):
    return await service.delete(manufacturer_id)
