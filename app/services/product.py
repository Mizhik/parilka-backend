from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Product
from app.repository.product import ProductRepository
from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.services.errors import ErrorNotFound
from app.utils.mappers import map_product_to_schema


class ProductService:
    def __init__(self, db: AsyncSession, repository: ProductRepository):
        self.db = db
        self.repository = repository

    async def get_popular_products(self, offset: Optional[int] = None, limit: Optional[int] = None):
        products = await self.repository.get_many(offset=offset, limit=limit, where=[Product.is_popular.is_(True)])
        products_schema = [map_product_to_schema(product) for product in products]
        return ResponseSchema(data=products_schema, message="Popular products")

    async def get_all_products(self, offset: Optional[int] = None, limit: Optional[int] = None):
        products = await self.repository.get_many(offset=offset, limit=limit)
        products_schema = [map_product_to_schema(product) for product in products]
        return ResponseSchema(data=products_schema, message="All products")

    async def get_one_product(self, product_id: UUID):
        product = await self.repository.get_one(id=product_id)
        print(product, "32")
        if not product:
            raise ErrorNotFound(f"Product with id: {product_id} does not exist.")

        product_schema = map_product_to_schema(product)
        print(product_schema, "37")

        return ResponseSchema[ProductSchema](data=product_schema, message="Product detail")

    async def create_product(self, body: ProductSchema):
        values = body.dict(exclude_unset=True)

        created_product = await self.repository.create(values)

        product_schema = ProductSchema.model_validate(created_product)

        return ResponseSchema[ProductSchema](data=product_schema, message="Product created.")

    async def edit_product(self, product_id: UUID, body: ProductSchema):
        if not await self.repository.get_one(id=product_id):
            raise ErrorNotFound(f"Product with id: {product_id} does not exist.")

        values = body.dict(exclude_unset=True)
        updated_product = await self.repository.update(values, id=product_id)
        product_schema = ProductSchema.model_validate(updated_product)

        return ResponseSchema[ProductSchema](data=product_schema, message="Product edited")

    async def delete_product(self, product_id: UUID):
        if not await self.repository.get_one(id=product_id):
            raise ErrorNotFound(f"Product with id: {product_id} does not exist.")

        await self.repository.delete(id=product_id)
        return ResponseSchema(data=None, message="Product deleted")
