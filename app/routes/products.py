from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database.db import get_db
from app.schemas.product import ProductBase
from app.repository.product import ProductRepository


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/popular", response_model=List[ProductBase])
async def get_popular_products(
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(10, gt=0),
        db: AsyncSession = Depends(get_db)
):
    product_repository = ProductRepository(db)
    return await product_repository.get_popular(offset=offset, limit=limit)
