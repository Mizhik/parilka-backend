from typing import Optional
from uuid import UUID
from pydantic import BaseModel, field_validator


class SubCategoryCreateSchema(BaseModel):
    title: str
    parent_id: UUID
    display_title: str

    @field_validator("title")
    @classmethod
    def lowercase_title(cls, v: str):
        return v.lower()


class SubCategoryEditSchema(BaseModel):
    title: Optional[str] = None
    parent_id: Optional[UUID] = None
    display_title: Optional[str] = None

    @field_validator("title")
    @classmethod
    def lowercase_title(cls, v: str):
        return v.lower()


class SubCategorySchema(BaseModel):
    id: UUID
    title: str
    parent_id: UUID
    display_title: str

    model_config = {
        "from_attributes": True,
    }
