from app.models.models import Product
from app.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Product)
