from uuid import UUID

from fastapi import APIRouter, Depends
from typing import List, Optional

from app.schemas.product import ProductBase, ProductResponse, ProductCreate
from app.services.dependencies import get_product_service
from app.services.product import ProductService
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/popular", response_model=List[ProductResponse])
async def get_popular_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_popular_products(offset=offset, limit=limit)


@router.get("", response_model=List[ProductResponse])
async def get_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_all_product(offset=offset, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
        product_id:UUID,
        product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_one_product(product_id)


@router.post("/add", response_model=ProductResponse)
async def create(
        body: ProductCreate,
        product_service: ProductService = Depends(get_product_service)
):
    created_product = await product_service.create_product(body)
    return created_product


@router.patch("/edit/{product_id}", response_model=ProductResponse)
async def edit(
        product_id: UUID,
        body: ProductBase,
        product_service: ProductService = Depends(get_product_service)
):
    edited_product = await product_service.edit_product(product_id, body)
    return edited_product


@router.delete("delete/{product_id}", response_model=ResponseSchema[ProductResponse])
async def delete(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
):
    deleted_product = await product_service.delete_product(product_id)

    return ResponseSchema[ProductResponse](
        message=f"Продукт {deleted_product.title} успішно видалено.",
        data=[]
    )
