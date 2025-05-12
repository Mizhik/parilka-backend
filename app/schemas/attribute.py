from decimal import Decimal
from typing import List, Optional, Self
from uuid import UUID
from pydantic import BaseModel, model_validator

from app.models.enums import AttributeGroupEnum
from app.schemas.image import ImageCreateSchema, ImageSchema


class AttributeSchema(BaseModel):
    id: UUID
    value: str
    price_modifier: Optional[Decimal] = None
    stock_quantity: int
    images: List[ImageSchema] = []

    class Config:
        from_attributes = True


class AttributeProductSchema(BaseModel):
    id: UUID
    value: str
    price_modifier: Optional[Decimal] = None
    stock_quantity: int

    class Config:
        from_attributes = True


class AttributeCreateSchema(BaseModel):
    attribute_group: AttributeGroupEnum
    value: str
    price_modifier: Optional[Decimal] = None
    stock_quantity: int
    images: List[ImageCreateSchema] = []

    @model_validator(mode="after")
    def check_main_image_count(self) -> Self:
        if len(self.images) == 0:
            return self

        main_count = 0
        for image in self.images:
            if image.is_main:
                main_count += 1

        if main_count > 1:
            raise ValueError("Attribute can only have 1 main image")

        if main_count == 0:
            self.images[0].is_main = True

        return self
