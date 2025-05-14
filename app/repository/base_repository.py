from typing import Any, Generic, List, Type, TypeVar
from uuid import UUID
from sqlalchemy import ColumnExpressionArgument, and_, delete, select, update
from sqlalchemy.engine import create
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, TypeVar

from sqlalchemy.sql.base import ExecutableOption

from app.models.base_model import Base
from app.repository.errors import DuplicateError, NotFoundError
from app.services.errors import HTTPErrorNotFound


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        db: AsyncSession,
        model: Type[ModelType],
        lazyopts: List[ExecutableOption] = [],
    ):
        self.db = db
        self.model = model
        self.lazyopts_ = lazyopts

    async def get_many(
        self,
        where: List[ColumnExpressionArgument] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        lazyopts: Optional[List[ExecutableOption]] = None,
        order_by: Optional[List[ColumnExpressionArgument]] = [],
        **params,
    ) -> list[ModelType]:
        stmt = select(self.model).options(*(lazyopts or self.lazyopts_))

        if where:
            stmt = stmt.where(*where)
        if params:
            stmt = stmt.filter_by(**params)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        if order_by:
            stmt = stmt.order_by(*order_by)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_one(
        self, where: List[ColumnExpressionArgument] = [], **params
    ) -> ModelType | None:
        query = select(self.model).options(*self.lazyopts_)

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

    async def create_unique(self, body: dict, unique_key: str):
        if await self.get_one(**{unique_key: body[unique_key]}):
            raise DuplicateError(
                f"{self.model.__name__} with {unique_key} '{body[unique_key]}' exists"
            )
        return await self.create(body)

    async def update(
        self, body: Any, where: List[ColumnExpressionArgument] = [], **params
    ) -> ModelType | None:
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

    async def get_one_or_404(
        self, options: List[ExecutableOption] = [], **params
    ) -> ModelType | None:
        result = await self.get_one(options=options, **params)
        if not result:
            raise NotFoundError
        return result

    async def delete(self, where: List[ColumnExpressionArgument] = [], **params):
        stmt = delete(self.model).filter_by(**params)

        if where:
            stmt = stmt.where(*where)
        if params:
            stmt = stmt.filter_by(**params)

        await self.db.execute(stmt)
        await self.db.commit()

    async def ensure_exists(self, id_: UUID):
        if not await self.get_one(id=id_):
            raise NotFoundError(f"{self.model.__name__} with id {id_} does not exist")

    async def ensure_exists_and_unique(
        self, id_: UUID, unique_field: str, unique_value: Any
    ):
        await self.ensure_exists(id_)

        conflict_filter = and_(
            getattr(self.model, unique_field) == unique_value, self.model.id != id_
        )

        if await self.get_one(where=[conflict_filter]):
            raise DuplicateError
