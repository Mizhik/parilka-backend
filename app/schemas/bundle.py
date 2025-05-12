from uuid import UUID
from pydantic import BaseModel


class BundleCreateSchema(BaseModel):
    product_id: UUID
