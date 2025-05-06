from app.models.models import SubCategory
from app.repository.base_repository import BaseRepository


class SubCategoryRepository(BaseRepository[SubCategory]):
    def __init__(self, db):
        super().__init__(db=db, model=SubCategory, lazyopts=[])
