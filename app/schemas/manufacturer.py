from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ManufacturerSchema(BaseModel):
    id: Optional[UUID] = None
    name: str = Field(max_length=50)

    class Config:
        from_attributes = True
