from typing import Dict, List
from sqlalchemy import update
from app.models.enums import ConstructorTag
from app.models.models import Constructor
from app.repository.base_repository import BaseRepository


class ConstructorRepository(BaseRepository[Constructor]):
    def __init__(self, db):
        super().__init__(db=db, model=Constructor)

    async def update(self, constructor_tag: ConstructorTag, components: List[Dict]):
        stmt = update(self.model).where(self.model.tag==constructor_tag).values(component_data=components).returning(self.model)

        result = await self.db.execute(stmt)
        updated_constructor = result.scalars().first()
        if updated_constructor:
            await self.db.commit()
        return updated_constructor

