import faker as faker_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Country

faker = faker_.Faker()

async def create_country(session: AsyncSession) -> Country:
    country = Country(name=faker.unique.country()[:50])
    session.add(country)
    await session.commit()
    await session.refresh(country)
    return country



