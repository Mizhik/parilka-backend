from typing import List
from uuid import UUID
from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import SubCategory
from app.repository.category import CategoryRepository
from app.repository.subcategory import SubCategoryRepository
from app.schemas.response import ResponseSchema
from app.schemas.subcategory import CreateSubCategorySchema, EditSubCategorySchema, SubCategorySchema
from app.services.errors import DuplicateError, ErrorNotFound, InternalServerError


class SubCategoryService:
    def __init__(self, db: AsyncSession, repository: SubCategoryRepository, category_repository: CategoryRepository):
        self.db = db
        self.repository = repository
        self.category_repository = category_repository

    async def get_all(self):
        res = await self.repository.get_many()
        subcategories = [SubCategorySchema.model_validate(sc) for sc in res]
        return ResponseSchema[List[SubCategorySchema]](data=subcategories)

    async def create(self, subcategory: CreateSubCategorySchema):
        if await self.repository.get_many(
            where=[or_(SubCategory.title == subcategory.title, SubCategory.display_title == subcategory.display_title)]
        ):
            raise DuplicateError(f"Sub-category already exists")
        if await self.category_repository.get_one(id=subcategory.parent_id) is None:
            raise ErrorNotFound(f"Parent category with id {subcategory.parent_id} does not exist")
        res = await self.repository.create(subcategory.model_dump())
        if res is None:
            raise InternalServerError("Could not create sub category")
        created_subcategory = SubCategorySchema.model_validate(res)
        return ResponseSchema(data=created_subcategory, message="Sub-category created")
    
    async def edit(self, id: UUID, subcategory: EditSubCategorySchema):
        existing = await self.repository.get_one(id=id)
        if existing is None:
            raise ErrorNotFound(f"Sub-category with id {id} does not exist")

        conditions = []
        if subcategory.title is not None and subcategory.title != existing.title:
            conditions.append(SubCategory.title == subcategory.title)
        if subcategory.display_title is not None and subcategory.display_title != existing.display_title:
            conditions.append(SubCategory.display_title == subcategory.display_title)

        if conditions:
            duplicates = await self.repository.get_many(where=[
                and_(
                    or_(*conditions), SubCategory.id != id,
                    SubCategory.id != id
                )
            ])
            if duplicates:
                raise DuplicateError("Sub category with the same tile or display title already exists")

        if not subcategory.parent_id is None and existing.parent_id != subcategory.parent_id:
            parent = await self.category_repository.get_one(id=subcategory.parent_id)
            if parent is None:
                raise ErrorNotFound(f"Parent category with id {subcategory.parent_id} does not exist")

        res = await self.repository.update(subcategory.model_dump(exclude_unset=True), id=id)
        if res is None:
            raise InternalServerError("Could not update subcateogry")
        updated_subcategory = SubCategorySchema.model_validate(res)
        return ResponseSchema(data=updated_subcategory, message="Subcategory updated")

    async def delete(self, id: UUID):
        existing = await self.repository.get_one(id=id)
        if existing is None:
            raise ErrorNotFound(f"Sub-category with id {id} does not exist")
        await self.repository.delete(id=id)
        return ResponseSchema(message="Sub-category deleted", data=None)
