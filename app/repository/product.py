from sqlalchemy.orm import selectinload

from app.models.models import Attribute, Image, Product
from app.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(db=db,
                         model=Product,
                         lazyopts=[selectinload(Product.images), selectinload(Product.attributes)]
                        )

    async def create(self, body: dict) -> Product | None:
        images = body.pop("images", [])
        attributes = body.pop("attributes", [])
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

        await self.db.commit()
        await self.db.refresh(product)
        return product
