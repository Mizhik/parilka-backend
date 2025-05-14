from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ProductStatus
from app.models.models import Product
from app.repository.product import ProductRepository
from app.schemas.main_page import MainPageSchema
from app.schemas.product import ProductSchema
from app.schemas.response import ResponseSchema
from app.utils.mappers import map_product_to_schema


class MainPageService:
    # NOTE: Later there will be banner repository, reviews repository
    def __init__(self, db: AsyncSession, product_repository: ProductRepository):
        self.db = db
        self.product_repository = product_repository

    async def get_main_page(self):
        popular = await self.product_repository.get_many(
            limit=5, status=ProductStatus.POPULAR, order_by=[Product.create_at.desc()]
        )
        catalogue = await self.product_repository.get_many(
            limit=5, status=ProductStatus.NONE, order_by=[Product.create_at.desc()]
        )
        discounts = await self.product_repository.get_many(
            limit=5, status=ProductStatus.DISCOUNT, order_by=[Product.create_at.desc()]
        )
        res = MainPageSchema(
            popular=[map_product_to_schema(p) for p in popular],
            catalogue=[map_product_to_schema(p) for p in catalogue],
            discounts=[map_product_to_schema(p) for p in discounts],
        )

        return ResponseSchema[MainPageSchema](data=res)
