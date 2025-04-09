from uuid import UUID

from fastapi import APIRouter, Depends, Body
from typing import List, Optional

from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.dependencies import get_product_service
from app.services.product import ProductService
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/popular", response_model=List[ProductSchema])
async def get_popular_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_popular_products(offset=offset, limit=limit)


@router.get("", response_model=List[ProductSchema])
async def get_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_all_products(offset=offset, limit=limit)


@router.get("/{product_id}", response_model=ResponseSchema[ProductSchema])
async def get_product(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_one_product(product_id)


@router.post("/add", response_model=ResponseSchema[ProductSchema])
async def create(
        body: ProductSchema,
        product_service: ProductService = Depends(get_product_service)
):
    return await product_service.create_product(body)


@router.patch("/edit/{product_id}", response_model=ResponseSchema[ProductSchema])
async def edit(
        product_id: UUID,
        body: ProductSchema,
        product_service: ProductService = Depends(get_product_service)
):
    return await product_service.edit_product(product_id, body)


@router.delete("/delete/{product_id}", response_model=ResponseSchema)
async def delete(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
):
    return await product_service.delete_product(product_id)
