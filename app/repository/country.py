
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Country
from app.repository.base_repository import BaseRepository


class CountryRepository(BaseRepository[Country]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, model = Country)

