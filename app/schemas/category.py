from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str = Field(max_length=50, min_length=1, description="Category title is required")

    class Config:
        from_attributes = True
