from enum import Enum, unique
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field, SerializeAsAny, field_validator, fields, validator

from app.models.enums import ConstructorType, ConstructorTag
from app.schemas.response import ResponseSchema

class PhotoType(str, Enum):
    BANNER = "banner"
    PRODUCT = "product"
    DISCOUNT = "discount"

class LinkType(str, Enum):
    NAVIGATE = "navigate"
    EXTERNAL = "external"

class ConstructorComponent(BaseModel):
    component_type: str
    order: int = Field()

class ConstructorTextBlock(ConstructorComponent):
    component_type: Literal[ConstructorType.TEXT]
    is_heading: bool = False
    text: str = Field(min_length=1, description="Text is required")
    color: str = ""

class ConstructorButton(ConstructorComponent):
    component_type: Literal[ConstructorType.BUTTON]
    text: str = Field(min_length=1, description="Text is required")
    href: str = Field(min_length=1, description="Href is required")
    link_type: LinkType = LinkType.NAVIGATE
    is_new_page: bool = False

class ConstructorPhoto(ConstructorComponent):
    id: str
    url: str
    type: Optional[PhotoType]

class ConstructorBannerPhoto(ConstructorPhoto):
    cover_gradient: str = ""
    components: Optional[List[ConstructorComponent]]

class ConstructorSchema(BaseModel):
    tag: ConstructorTag
    component_data: List[Union[ConstructorButton, ConstructorTextBlock]]
    model_config = {
        "from_attributes": True,
    }

    @field_validator("component_data")
    @classmethod
    def no_order_duplicates(cls, components):
        if components is None:
            return components
        orders = [component.order for component in components]
        if len(orders) != (len(set(orders))):
            raise ValueError("Duplicate 'order' values found in component data")
        return components


class ConstructorResponseSchema(ResponseSchema):
    data: dict[
        ConstructorTag,
        Optional[ConstructorSchema]
    ]
