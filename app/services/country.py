from uuid import UUID
from sqlalchemy.orm import exc
from app.repository.country import CountryRepository
from app.repository.errors import DuplicateError, NotFoundError
from app.schemas.country import CountryCreateSchema, CountrySchema
from app.schemas.response import ResponseSchema
from app.services.errors import HTTPDuplicateError, HTTPErrorNotFound


class CountryService:
    def __init__(self, db, repository: CountryRepository) -> None:
        self.db = db
        self.repository = repository

    async def get_all(self):
        res = await self.repository.get_many()
        countries = [CountrySchema.model_validate(c) for c in res]
        return ResponseSchema(data=countries)
    
    async def create(self, country: CountryCreateSchema):
        try:
            res = await self.repository.create_unique(country.model_dump(), "name")
            created_country = CountrySchema.model_validate(res)
            return ResponseSchema(data=created_country, message="Country created")
        except DuplicateError as e:
            raise HTTPDuplicateError(message=str(e))

    async def edit(self, id: UUID, country: CountryCreateSchema):
        try:
            await self.repository.ensure_exists_and_unique(id, "name", country.name)
            res = await self.repository.update(country.model_dump(), id=id)
            updated_country = CountrySchema.model_validate(res)
            return ResponseSchema(data=updated_country, message="Country updated")
        except NotFoundError as e:
            raise HTTPErrorNotFound(message=str(e))
        except DuplicateError as e:
            raise HTTPDuplicateError(message=str(e))

    async def delete(self, id: UUID):
        try:
            await self.repository.ensure_exists(id)
            await self.repository.delete(id=id)
            return ResponseSchema(message="Country deleted", data=None)
        except NotFoundError as e:
            raise HTTPErrorNotFound(message=str(e))
        

