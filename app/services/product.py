from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.enums import ProductStatus
from app.models.models import Product
from app.repository.product import ProductRepository
from app.schemas.product import ProductCreateSchema, ProductDetailsSchema, ProductSchema
from app.schemas.response import ResponseSchema
from app.services.errors import HTTPErrorNotFound, HTTPInternalServerError
from app.utils.mappers import map_product_to_detailed_schema, map_product_to_schema


class ProductService:
    def __init__(self, db: AsyncSession, repository: ProductRepository):
        self.db = db
        self.repository = repository

    async def get_popular_products(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ):
        products = await self.repository.get_many(
            offset=offset, limit=limit, where=[Product.status == ProductStatus.POPULAR]
        )
        products_schema = [map_product_to_schema(product) for product in products]
        return ResponseSchema(data=products_schema, message="Popular products")

    async def get_all_products(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ):
        products = await self.repository.get_many(
            offset=offset,
            limit=limit,
            lazyopts=[selectinload(Product.images), joinedload(Product.category)],
        )
        products_schema = [map_product_to_schema(product) for product in products]
        return ResponseSchema(data=products_schema, message="All products")

    async def get_one_product(self, product_id: UUID):
        product = await self.repository.get_one(id=product_id)
        if not product:
            raise HTTPErrorNotFound(f"Product with id: {product_id} does not exist.")

        product_schema = map_product_to_detailed_schema(product)

        return ResponseSchema(data=product_schema, message="Product detail")

    async def create_product(self, body: ProductCreateSchema):
        values = body.dict(exclude_unset=True)

        created_product = await self.repository.create(values)

        if not created_product:
            raise HTTPInternalServerError()

        product = await self.repository.get_one(id=created_product.id)

        if not product:
            raise HTTPInternalServerError("Failed to get created product")

        product_schema = map_product_to_detailed_schema(product)

        return ResponseSchema[ProductDetailsSchema](
            data=product_schema, message="Product created."
        )

    async def edit_product(self, product_id: UUID, body: ProductDetailsSchema):
        if not await self.repository.get_one(id=product_id):
            raise HTTPErrorNotFound(f"Product with id: {product_id} does not exist.")

        values = body.dict(exclude_unset=True)
        updated_product = await self.repository.update(values, id=product_id)

        if not updated_product:
            raise HTTPInternalServerError()

        product = await self.repository.get_one(id=updated_product.id)

        if not product:
            raise HTTPInternalServerError("Failed to get created product")

        product_schema = map_product_to_detailed_schema(product)

        return ResponseSchema[ProductDetailsSchema](
            data=product_schema, message="Product edited"
        )

    async def delete_product(self, product_id: UUID):
        if not await self.repository.get_one(id=product_id):
            raise HTTPErrorNotFound(f"Product with id: {product_id} does not exist.")

        await self.repository.delete(id=product_id)
        return ResponseSchema(data=None, message="Product deleted")
