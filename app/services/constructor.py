from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ConstructorTag
from app.models.models import Constructor
from app.repository.constructor import ConstructorRepository
from app.schemas.constructor import ConstructorComponent, ConstructorSchema
from app.schemas.response import ResponseSchema
from app.services.errors import BadRequestError


class ConstructorService:
    def __init__(self, db: AsyncSession, repository: ConstructorRepository):
        self.db = db
        self.repository = repository


    async def get_all(self):
        res = await self.repository.get_many()
        constructors = [ConstructorSchema.model_validate(constructor) for constructor in res]
        constructors_dict: Dict[ConstructorTag, ConstructorSchema] = {
            constructor.tag: constructor for constructor in constructors
        }
        return ResponseSchema[Dict[ConstructorTag, ConstructorSchema]](data=constructors_dict)

    async def get_by_tag(self, constructor_tag: ConstructorTag):
        if constructor_tag not in ConstructorTag:
            raise BadRequestError(f"Invalid tag {constructor_tag}")
        res = await self.repository.get_one(tag=constructor_tag)
        constructor_schema = ConstructorSchema.model_validate(res)
        return ResponseSchema[List[ConstructorComponent]](data=constructor_schema.component_data)
    
    async def edit(self, constructor_tag: ConstructorTag, body: List[ConstructorComponent]) -> ResponseSchema[ConstructorSchema]:
        if constructor_tag not in ConstructorTag:
            raise BadRequestError(f"Invalid tag {constructor_tag}")

        orders = [component.order for component in body]
        if len(orders) != (len(set(orders))):
            raise BadRequestError(f"Duplicate 'order' found")

        components: List[Dict] = [c.model_dump() for c in body] 
        res = await self.repository.update(components, tag=constructor_tag)
        constructor_schema = ConstructorSchema.model_validate(res)
        return ResponseSchema(data=constructor_schema, message="Constructor edited")



