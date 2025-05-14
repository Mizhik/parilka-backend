from uuid import UUID
from pydantic import BaseModel, Field


class ManufacturerSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class ManufacturerCreateSchema(BaseModel):
    name: str = Field(max_length=100, min_length=1)
    model_config = {"from_attributes": True}
