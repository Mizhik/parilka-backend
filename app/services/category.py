from typing import List
from uuid import UUID 
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.repository.category import CategoryRepository
from app.schemas.category import CategorySchema
from app.schemas.response import ResponseSchema
from app.services.errors import DuplicateError, ErrorNotFound


class CategoryService:
    def __init__(self, db: AsyncSession, repository: CategoryRepository):
        self.db = db
        self.repository = repository
    
    async def get_all(self):
        res = await self.repository.get_many()
        categories = [CategorySchema.model_validate(category) for category in res]
        return ResponseSchema[List[CategorySchema]](data=categories, message="success")

    async def create(self, body: CategorySchema):
        if await self.repository.get_by_title(body.title):
            raise DuplicateError(f"Category with title: {body.title} already exists")
        category = body.model_dump()
        res = await self.repository.create(category)
        category_schema = CategorySchema.model_validate(res)
        return ResponseSchema[CategorySchema](data=category_schema)
    
    async def edit(self, category_id: UUID, body: CategorySchema):
        if not await self.repository.get_one(id=category_id):
            raise ErrorNotFound(f"Category with id: {category_id} does not exist")

        category = body.model_dump(exclude_unset=True)
        res = await self.repository.update(category_id, category)
        category_schema = CategorySchema.model_validate(res)
        return ResponseSchema[CategorySchema](data=category_schema)
    
    async def delete(self, category_id: UUID):
        if not await self.repository.get_one(id=category_id):
            raise ErrorNotFound(f"Category with id: {category_id} does not exist")
