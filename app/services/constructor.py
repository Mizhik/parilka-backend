from typing import List, Union
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ConstructorTag
from app.repository.constructor import ConstructorRepository
from app.schemas.constructor import ConstructorResponseSchema, ConstructorSchema
from app.schemas.response import ResponseSchema
from app.services.errors import DuplicateError


class ConstructorService:
    def __init__(self, db: AsyncSession, repository: ConstructorRepository):
        self.db = db
        self.repository = repository

    async def get_all(self):
        res = await self.repository.get_many()
        print(res)
        constructors = {
            ConstructorTag.TOP_BANNER: next((item for item in res if item.tag == ConstructorTag.TOP_BANNER), None),
            ConstructorTag.BOTTOM_BANNER: None,
            ConstructorTag.ACCORDION: None
        }

        return ConstructorResponseSchema(data=constructors)
    
    async def create(self, body: ConstructorSchema):
        if body.tag == ConstructorTag.TOP_BANNER or body.tag == ConstructorTag.BOTTOM_BANNER:
            if await self.repository.get_one(tag=body.tag):
                raise DuplicateError(f"There could be only 1 constructor with tag: {body.tag.value}")
        print(body)
        constructor = body.model_dump()
        res = await self.repository.create(constructor)
        constructor_schema = ConstructorSchema.model_validate(res)
        return ResponseSchema[ConstructorSchema](data=constructor_schema, message="Constructor created")
