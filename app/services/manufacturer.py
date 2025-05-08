from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.errors import DuplicateError, NotFoundError
from app.repository.manufacturer import ManufacturerRepository
from app.schemas.manufacturer import ManufacturerCreateSchema, ManufacturerSchema
from app.schemas.response import ResponseSchema
from app.services.errors import HTTPDuplicateError, HTTPErrorNotFound


class ManufacturerService:
    def __init__(self, db: AsyncSession, repository: ManufacturerRepository) -> None:
        self.db = db
        self.repository = repository

    async def get_all(self):
        res = await self.repository.get_many()
        manufacturers = [ManufacturerSchema.model_validate(m) for m in res]
        return ResponseSchema(data=manufacturers)

    async def create(self, manufacturer: ManufacturerCreateSchema):
        try:
            res = await self.repository.create_unique(manufacturer.model_dump(), unique_key="name")
            created_manufacturer = ManufacturerSchema.model_validate(res)
            return ResponseSchema(data=created_manufacturer, message="Manufacturer created")
        except DuplicateError as e:
            raise HTTPDuplicateError(message=str(e))


    async def edit(self, id: UUID, manufacturer: ManufacturerCreateSchema):
        try:
            await self.repository.ensure_exists_and_unique(id, "name", manufacturer.name)
            res = await self.repository.update(manufacturer.model_dump(), id=id)
            updated_manufacturer = ManufacturerSchema.model_validate(res)
            return ResponseSchema(data=updated_manufacturer, message="Manufacturer updated")
        except NotFoundError as e:
            raise HTTPErrorNotFound(message=str(e))
        except DuplicateError as e:
            raise HTTPDuplicateError(message=str(e))
        
    async def delete(self, id: UUID):
        try:
            await self.repository.ensure_exists(id)
            await self.repository.delete(id=id)
            return ResponseSchema(message="Manufacturer deleted", data=None)
        except NotFoundError as e:
            raise HTTPErrorNotFound(message=str(e))

