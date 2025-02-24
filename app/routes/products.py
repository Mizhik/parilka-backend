from fastapi import APIRouter, Depends
from typing import List, Optional

from app.schemas.product import ProductBase
from app.repository.product import ProductRepository
from app.services.dependencies import get_product_service
from app.services.product import ProductService


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/popular", response_model=List[ProductBase])
async def get_popular_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_popular_products(offset=offset, limit=limit)
