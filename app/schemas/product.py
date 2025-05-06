from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Self

from pydantic.json_schema import SkipJsonSchema

from app.models.enums import ProductStatus as StatusEnum
from app.schemas.image import ImageSchema
from app.schemas.attribute import AttributeSchema

class ProductSchema(BaseModel):
    id: Optional[UUID] = None
    title: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    main_image: Optional[ImageSchema] = None
    discount_price: Optional[Decimal] = Field(default=None, gt=0)
    is_available: bool = Field(default=True)
    status: StatusEnum = StatusEnum.NONE
    category: Optional[str] = None
    sub_category: Optional[str] = None

    class Config:
        from_attributes = True

class ProductDetailsSchema(ProductSchema):
    main_image: SkipJsonSchema[Optional[ImageSchema]] = Field(default=None, exclude=True)
    stock_quantity: int = Field(ge=0)
    country_of_origin_id: UUID
    manufacturer_id: UUID
    stock_quantity: int = Field(ge=0)
    description: str = Field(min_length=1, max_length=255)
    images: List[ImageSchema] = []
    attributes: List[AttributeSchema] = []
    category_id: UUID
    subcategory_id: Optional[UUID] = None

class ProductCreateSchema(ProductDetailsSchema):
    id: SkipJsonSchema[Optional[UUID]] = Field(default=None, exclude=True)
    category: SkipJsonSchema[Optional[str]] = Field(default=None, exclude=True)
    sub_category: SkipJsonSchema[Optional[str]] = Field(default=None, exclude=True)
    category_id: UUID
    subcategory_id: Optional[UUID] = None
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
