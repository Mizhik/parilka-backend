from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: Optional[UUID] = None
    title: str = Field(max_length=50, min_length=1, description="Category title is required")

    class Config:
        from_attributes = True
