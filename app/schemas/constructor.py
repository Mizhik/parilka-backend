from enum import Enum
from typing import List, Literal, Union
from pydantic import BaseModel, Field

from app.models.enums import ConstructorType, ConstructorTag

class PhotoType(str, Enum):
    BANNER = "banner"
    PRODUCT = "product"
    DISCOUNT = "discount"

class LinkType(str, Enum):
    NAVIGATE = "navigate"
    EXTERNAL = "external"

class _ConstructorComponent(BaseModel):
    component_type: str
    order: int = Field()

class ConstructorTextBlock(_ConstructorComponent):
    component_type: Literal[ConstructorType.TEXT]
    is_heading: bool = False
    text: str = Field(min_length=1, description="Text is required")
    color: str = ""

class ConstructorButton(_ConstructorComponent):
    component_type: Literal[ConstructorType.BUTTON]
    text: str = Field(min_length=1, description="Text is required")
    href: str = Field(min_length=1, description="Href is required")
    link_type: LinkType = LinkType.NAVIGATE
    is_new_page: bool = False

ConstructorComponent = Union[ConstructorButton, ConstructorTextBlock]

class ConstructorSchema(BaseModel):
    tag: ConstructorTag
    component_data: List[ConstructorComponent]
    model_config = {
        "from_attributes": True,
    }
