from typing import Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, TypeVar

from app.models.base_model import Base
from app.services.errors import ErrorNotFound


ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.db = db
        self.model = model

    async def get_many(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[ModelType]:
        stmt = select(self.model)
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_one(self, **params) -> ModelType | None:
        query = select(self.model).filter_by(**params)
        result = await self.db.execute(query)
        db_row = result.unique().scalar_one_or_none()
        return db_row

    async def create(self, body: dict) -> ModelType | None:
        result = self.model(**body)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def get_one_or_404(self, params: dict) -> ModelType | None:
        result = await self.get_one(**params)
        if not result:
            raise ErrorNotFound
        return result
