from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List

from app.schemas.image import ImageSchema
from app.schemas.country import CountrySchema
from app.schemas.manufacturer import ManufacturerSchema
from app.schemas.category import CategorySchema
from app.schemas.attribute import AttributeSchema


class ProductBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    is_available: bool = Field(default=True)
    is_popular: bool = Field(default=False)
    is_new: bool = Field(default=True)
    category_id: UUID
    country_id: UUID
    manufacturer_id: UUID
    images: List[ImageSchema] = []
    attributes: List[AttributeSchema] = []

    class Config:
        from_attributes = True
