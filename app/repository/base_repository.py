from typing import Any, Generic, List, Type, TypeVar
from sqlalchemy import ColumnExpressionArgument, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, TypeVar

from sqlalchemy.sql.base import ExecutableOption

from app.models.base_model import Base
from app.services.errors import ErrorNotFound


ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType],  lazyopts: List[ExecutableOption] = []):
        self.db = db
        self.model = model
        self.lazyopts = lazyopts 

    async def get_many(
        self, 
        where: List[ColumnExpressionArgument] = [],
        offset: Optional[int] = None, 
        limit: Optional[int] = None,
        **params,
    ) -> list[ModelType]:
        stmt = select(self.model).options(*self.lazyopts)

        if where:
            stmt = stmt.where(*where)
        if params:
            stmt = stmt.filter_by(**params)
        if offset is not None: 
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_one(self, where: List[ColumnExpressionArgument] = [], **params) -> ModelType | None:
        query = select(self.model).options(*self.lazyopts)

        if where:
            query = query.where(*where)
        if params:
            query = query.filter_by(**params)

        result = await self.db.execute(query)
        db_row = result.unique().scalar_one_or_none()
        return db_row

    async def create(self, body: dict) -> ModelType | None:
        result = self.model(**body)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update(self, body: Any, where: List[ColumnExpressionArgument] = [], **params) -> ModelType | None:
        stmt = update(self.model).values(**body).returning(self.model)

        if where:
            stmt = stmt.where(*where)
        if params:
            stmt = stmt.filter_by(**params)

        result = await self.db.execute(stmt)
        updated_model = result.scalars().first()
        if updated_model:
            await self.db.commit()
        return updated_model

    async def get_one_or_404(self, options: List[ExecutableOption] = [], **params) -> ModelType | None:
        result = await self.get_one(options=options, **params)
        if not result:
            raise ErrorNotFound
        return result
    
    async def delete(self, where: List[ColumnExpressionArgument] = [], **params):
        stmt = delete(self.model).filter_by(**params)

        if where:
            stmt = stmt.where(*where)
        if params:
            stmt = stmt.filter_by(**params)

        await self.db.execute(stmt)
        await self.db.commit()
