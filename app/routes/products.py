from uuid import UUID

from fastapi import APIRouter, Depends
from typing import List, Optional
from fastapi_cache.decorator import cache

from app.schemas.product import ProductCreateSchema, ProductDetailsSchema, ProductSchema
from app.schemas.response import ResponseSchema
from app.services.dependencies import get_product_service
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/popular", response_model=ResponseSchema[List[ProductSchema]])
async def get_popular_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_popular_products(offset=offset, limit=limit)


@router.get("", response_model=ResponseSchema[List[ProductSchema]])
@cache(expire=60 * 5)
async def get_products(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_all_products(offset=offset, limit=limit)


@router.get("/{product_id}", response_model=ResponseSchema[ProductDetailsSchema])
@cache(expire=60 * 2)
async def get_product(
    product_id: UUID, product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_one_product(product_id=product_id)


@router.post("/add", response_model=ResponseSchema[ProductDetailsSchema])
async def create(
    body: ProductCreateSchema,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_product(body)


# @router.patch("/edit/{product_id}", response_model=ResponseSchema[ProductDetailsSchema])
# async def edit(
#         product_id: UUID,
#         body: ProductDetailsSchema,
#         product_service: ProductService = Depends(get_product_service)
# ):
#     return await product_service.edit_product(product_id, body)
#


@router.delete("/delete/{product_id}", response_model=ResponseSchema)
async def delete(
    product_id: UUID, product_service: ProductService = Depends(get_product_service)
):
    return await product_service.delete_product(product_id)
