from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from decimal import Decimal


class ProductFilterParams(BaseModel):
    price_min: Optional[Decimal] = Field(default=None, ge=0)
    price_max: Optional[Decimal] = Field(default=None, gt=0)
    manufacturer_id: Optional[List[UUID]] = None
    limit: Optional[int] = Field(default=16, gt=0, le=100)
    offset: Optional[int] = Field(default=0, ge=0)
