from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List, Optional


# Схеми для пов'язаних моделей
class ImageSchema(BaseModel):
    id: UUID
    url: str


class CategorySchema(BaseModel):
    id: UUID
    name: str


class CountrySchema(BaseModel):
    id: UUID
    name: str


class ManufacturerSchema(BaseModel):
    id: UUID
    name: str


class ProductBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    is_available: bool = Field(default=True)


class ProductResponse(ProductBase):
    id: UUID
    images: List[ImageSchema] = []
    category: CategorySchema
    country: CountrySchema
    manufacturer: ManufacturerSchema

    class Config:
        from_attributes = True
