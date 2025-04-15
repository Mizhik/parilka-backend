from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class AttributeSchema(BaseModel):
    id: Optional[UUID] = None
    title: str = Field(max_length=100)
    value: str

    class Config:
        from_attributes = True
