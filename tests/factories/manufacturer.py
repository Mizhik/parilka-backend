import faker as faker_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Manufacturer

faker = faker_.Faker()

async def create_manufacturer(session: AsyncSession) -> Manufacturer:
    manufacturer = Manufacturer(name=faker.company())
    session.add(manufacturer)
    await session.commit()
    await session.refresh(manufacturer)
    return manufacturer
