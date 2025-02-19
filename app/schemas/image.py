from uuid import UUID
from pydantic import BaseModel, Field


class ImageSchema(BaseModel):
    id: UUID
    url: str = Field(max_length=500)
    product_id: UUID

    class Config:
        from_attributes = True
