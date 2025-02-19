from uuid import UUID
from pydantic import BaseModel, Field


class ManufacturerSchema(BaseModel):
    id: UUID
    name: str = Field(max_length=50)

    class Config:
        from_attributes = True
