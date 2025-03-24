from typing import List 
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from app.models.models import Category
from app.repository.category import CategoryRepository
from app.schemas.category import CategorySchema
from app.schemas.response import ResponseSchema


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
            raise HTTPException(
                HTTP_409_CONFLICT,
                detail=f"Category with the name '{body.title}' already exists"
            )

        if not body.title:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail="Category title cannot be empty"
            )
        category = body.model_dump()
        res = await self.repository.create(category)
        category = CategorySchema.model_validate(res)
        return ResponseSchema[CategorySchema](data=category)
