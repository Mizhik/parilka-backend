from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.enums import ProductStatus as StatusEnum
from app.schemas.image import ImageSchema
from app.schemas.country import CountrySchema
from app.schemas.manufacturer import ManufacturerSchema
from app.schemas.category import CategorySchema
from app.schemas.attribute import AttributeSchema


class ProductSchema(BaseModel):
    id: Optional[UUID] = None
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    is_available: bool = Field(default=True)
    status: StatusEnum = StatusEnum.NONE
    category_id: UUID
    country_of_origin_id: UUID
    manufacturer_id: UUID
    images: List[ImageSchema] = []
    attributes: List[AttributeSchema] = []

    class Config:
        from_attributes = True
