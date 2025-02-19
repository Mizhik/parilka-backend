from uuid import UUID
from pydantic import BaseModel, Field


class AttributeSchema(BaseModel):
    id: UUID
    title: str = Field(max_length=100)
    value: str

    class Config:
        from_attribute = True
