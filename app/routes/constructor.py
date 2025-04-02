from fastapi import APIRouter, Depends

from app.schemas.constructor import ConstructorResponseSchema, ConstructorSchema
from app.schemas.response import ResponseSchema
from app.services.constructor import ConstructorService
from app.services.dependencies import get_constructor_service
router = APIRouter(prefix="/constructor", tags=["Constructor"])


@router.get("/", response_model=ConstructorResponseSchema)
async def get_constructor(constructor_service: ConstructorService = Depends(get_constructor_service)):
    return await constructor_service.get_all()
    
@router.post("/add", response_model=ResponseSchema[ConstructorSchema])
async def create_constructor(body: ConstructorSchema, constructor_service: ConstructorService = Depends(get_constructor_service)):
    return await constructor_service.create(body)
