from typing import List
from sqlalchemy import ColumnExpressionArgument, select
from sqlalchemy.orm import joinedload, selectinload

from app.models.models import Attribute, BundleContent, Image, Product
from app.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(
            db=db,
            model=Product,
            lazyopts=[
                selectinload(Product.images),
                selectinload(Product.attributes),
                joinedload(Product.category),
                selectinload(Product.bundle_items).selectinload(BundleContent.product),
                joinedload(Product.country),
                joinedload(Product.manufacturer),
            ],
        )

    async def create(self, body: dict) -> Product | None:
        images = body.pop("images", [])
        attributes = body.pop("attributes", [])
        bundle_items = body.pop("bundle_items", [])
        product = Product(**body)
        self.db.add(product)

        for image_data in images:
            image = Image(**image_data)
            product.images.append(image)

        for attribute_data in attributes:
            attr_images = attribute_data.pop("images", [])
            attribute = Attribute(**attribute_data)
            for image_data in attr_images:
                attribute.images.append(Image(**image_data))
            product.attributes.append(attribute)

        for bundle_item in bundle_items:
            bundle_content = BundleContent(**bundle_item)
            product.bundle_items.append(bundle_content)

        await self.db.commit()
        await self.db.refresh(product)
        return product
