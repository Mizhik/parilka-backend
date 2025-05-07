from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ImageSchema(BaseModel):
    id: Optional[UUID] = None
    image_url: str
    is_main: bool = False
    product_id: Optional[UUID] = None
    attribute_id: Optional[UUID] = None

    class Config:
        from_attributes = True
