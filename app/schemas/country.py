from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CountrySchema(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class CountryCreateSchema(BaseModel):
    name: str = Field(max_length=50, min_length=1)

    model_config = {
        "from_attributes": True
    }
