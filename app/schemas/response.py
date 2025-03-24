from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class ResponseSchema(BaseModel, Generic[T]):
    message: Optional[str] = Field(default="success")
    data: T | List[T]

    class Config:
        from_attributes = True
