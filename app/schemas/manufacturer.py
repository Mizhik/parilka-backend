from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.product import ProductSchema


class ManufacturerSchema(BaseModel):
    id: UUID
    name: str
    products: List[ProductSchema] = []

    class Config:
        from_attributes = True


class ManufacturerCreateSchema(BaseModel):
    name: str = Field(max_length=100)
    model_config = {
        "from_attributes": True
    }
