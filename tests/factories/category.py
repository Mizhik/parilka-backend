import faker as faker_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category

faker = faker_.Faker()

async def create_category(session: AsyncSession) -> Category:
    category = Category(title=faker.word())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

