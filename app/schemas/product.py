from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator
from typing import Dict, List, Optional, Self

from app.models.enums import AttributeGroupEnum, ProductStatus as StatusEnum
from app.schemas.bundle import BundleCreateSchema
from app.schemas.image import ImageCreateSchema, ImageSchema
from app.schemas.attribute import (
    AttributeCreateSchema,
    AttributeProductSchema,
)
from app.schemas.category import CategorySchema
from app.schemas.subcategory import SubCategorySchema


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
    title: str
    price: Decimal
    sku: str
    stock_quantity: int
    country_of_origin_id: UUID
    manufacturer_id: UUID
    stock_quantity: int
    description: str
    images: List[ImageSchema] = []
    attributes: Dict[AttributeGroupEnum, List[AttributeProductSchema]] = {}
    subcategory_id: Optional[UUID]
    category: CategorySchema
    sub_category: Optional[SubCategorySchema]
    is_available: bool
    status: StatusEnum
    bundle_items: List[ProductSchema] = []

    class Config:
        from_attributes = True


class ProductCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    category_id: UUID
    sku: str
    subcategory_id: Optional[UUID] = None
    discount_price: Optional[Decimal] = Field(default=None, gt=0)
    is_available: bool = Field(default=True)
    is_bundle: bool = False
    status: StatusEnum = StatusEnum.NONE
    stock_quantity: int = Field(ge=0)
    country_of_origin_id: UUID
    manufacturer_id: UUID
    description: str = Field(min_length=1, max_length=255)
    images: List[ImageCreateSchema] = []
    attributes: List[AttributeCreateSchema] = []
    bundle_items: List[BundleCreateSchema] = []

    @model_validator(mode="after")
    def check_main_image_count(self) -> Self:
        all_images = [(img, "product") for img in self.images] + [
            (img, "attribute") for attr in self.attributes for img in attr.images
        ]
        if len(all_images) == 0:
            return self

        main_images = [img for img, _ in all_images if img.is_main]

        if len(main_images) > 1:
            raise ValueError("Product can only have 1 main image")

        if not main_images:
            for img, origin in all_images:
                if origin == "product":
                    img.is_main = True
                    break
                else:
                    if all_images:
                        all_images[0][0].is_main = True

        return self
