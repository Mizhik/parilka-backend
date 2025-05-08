from typing import List
from uuid import UUID
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Category
from app.repository.category import CategoryRepository
from app.schemas.category import CategoryCreateSchema, CategorySchema
from app.schemas.response import ResponseSchema
from app.services.errors import HTTPDuplicateError, HTTPErrorNotFound


class CategoryService:
    def __init__(self, db: AsyncSession, repository: CategoryRepository):
        self.db = db
        self.repository = repository

    async def get_all(self):
        res = await self.repository.get_many()
        categories = [CategorySchema.model_validate(category) for category in res]
        return ResponseSchema[List[CategorySchema]](data=categories)

    async def create(self, body: CategoryCreateSchema):
        if await self.repository.get_one(title=body.title):
            raise HTTPDuplicateError(
                f"Category with title: {body.title} already exists"
            )
        category = body.model_dump()
        res = await self.repository.create(category)
        category_schema = CategorySchema.model_validate(res)
        return ResponseSchema[CategorySchema](
            data=category_schema, message="Category created"
        )

    async def edit(self, category_id: UUID, body: CategoryCreateSchema):
        if not await self.repository.get_one(id=category_id):
            raise HTTPErrorNotFound(f"Category with id: {category_id} does not exist")
        if await self.repository.get_one(
            where=[and_(Category.title == body.title, Category.id != category_id)]
        ):
            raise HTTPDuplicateError(f"Category with title {body.title} already exists")

        category = body.model_dump(exclude_unset=True)
        res = await self.repository.update(category, id=category_id)
        category_schema = CategorySchema.model_validate(res)
        return ResponseSchema[CategorySchema](
            data=category_schema, message="Category edited"
        )

    async def delete(self, category_id: UUID):
        if not await self.repository.get_one(id=category_id):
            raise HTTPErrorNotFound(f"Category with id: {category_id} does not exist")

        await self.repository.delete(id=category_id)
        return ResponseSchema(data=None, message="Category deleted")
