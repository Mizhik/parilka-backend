


from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Manufacturer
from app.repository.base_repository import BaseRepository


class ManufacturerRepository(BaseRepository[Manufacturer]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, model = Manufacturer)

