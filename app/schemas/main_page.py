from typing import List
from pydantic import BaseModel

from app.schemas.product import ProductSchema


class MainPageSchema(BaseModel):
    popular: List[ProductSchema]
    catalogue: List[ProductSchema]
    discounts: List[ProductSchema]
