from uuid import UUID
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: UUID
    title: str = Field(max_length=50)

    class Config:
        from_attributes = True
