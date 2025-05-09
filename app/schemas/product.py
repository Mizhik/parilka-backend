from collections import defaultdict
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, computed_field, model_validator
from typing import Dict, List, Optional, Self

from app.models.enums import AttributeGroupEnum, ProductStatus as StatusEnum
from app.schemas.image import ImageCreateSchema, ImageSchema
from app.schemas.attribute import AttributeCreateSchema, AttributeSchema
from app.schemas.category import CategorySchema

class ProductSchema(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    main_image: Optional[ImageSchema] = None
    discount_price: Optional[Decimal] = Field(default=None, gt=0)
    is_available: bool = Field(default=True)
    status: StatusEnum = StatusEnum.NONE

    class Config:
        from_attributes = True

class ProductDetailsSchema(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    country_of_origin_id: UUID
    manufacturer_id: UUID
    stock_quantity: int = Field(ge=0)
    description: str = Field(min_length=1, max_length=255)
    images: List[ImageSchema] = []
    attributes: Dict[AttributeGroupEnum, List[AttributeSchema]] = {}
    category_id: UUID = Field(exclude=True)
    subcategory_id: Optional[UUID] = Field(default=None, exclude=True)
    category: CategorySchema 
    sub_category: Optional[str] = None
    is_available: bool = Field(default=True)
    status: StatusEnum = StatusEnum.NONE

    class Config:
        from_attributes = True

class ProductCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    category_id: UUID
    subcategory_id: Optional[UUID] = None
    discount_price: Optional[Decimal] = Field(default=None, gt=0)
    is_available: bool = Field(default=True)
    status: StatusEnum = StatusEnum.NONE
    stock_quantity: int = Field(ge=0)
    country_of_origin_id: UUID
    manufacturer_id: UUID
    description: str = Field(min_length=1, max_length=255)
    images: List[ImageCreateSchema] = []
    attributes: List[AttributeCreateSchema] = []

    @model_validator(mode='after')
    def check_main_image_count(self) -> Self:
        if len(self.images) == 0:
            return self

        main_count = 0
        for image in self.images:
            if image.is_main:
                main_count += 1

        if main_count > 1:
            raise ValueError("Product can only have 1 main image")

        if main_count == 0:
            self.images[0].is_main = True

        return self
