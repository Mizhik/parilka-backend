import faker as faker_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Category, SubCategory

faker = faker_.Faker()

async def create_subcategory(session: AsyncSession, category: Category) -> SubCategory:
    sub_categories = SubCategory(parent_id=category.id, title=faker.word(), display_title=faker.word())
    session.add(sub_categories)
    await session.commit()
    await session.refresh(sub_categories)
    return sub_categories
