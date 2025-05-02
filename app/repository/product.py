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
        
        for image in images:
            product.images.append(Image(**image))

        for attribute in attributes:
            product.attributes.append(Attribute(**attribute))

        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
