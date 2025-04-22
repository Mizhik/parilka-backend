from sqlalchemy.orm import selectinload

from app.models.models import Product
from app.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(db=db,
                         model=Product,
                         lazyopts=[selectinload(Product.images), selectinload(Product.attributes)]
                        )
