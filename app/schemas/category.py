from uuid import UUID
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True


class CategoryCreateSchema(BaseModel):
    title: str = Field(
        max_length=50, min_length=1, description="Category title is required"
    )

    class Config:
        from_attributes = True
