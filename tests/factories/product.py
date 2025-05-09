import faker as faker_
from ast import Attribute
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enums import Status

from app.models.models import (
    Category,
    Country,
    Image,
    Manufacturer,
    Product,
    SubCategory,
)
from tests.factories.category import create_category
from tests.factories.country import create_country
from tests.factories.manufacturer import create_manufacturer


faker = faker_.Faker()


async def create_product(
    session: AsyncSession,
    *,
    category: Optional[Category] = None,
    subcategory: Optional[SubCategory] = None,
    country: Optional[Country] = None,
    manufacturer: Optional[Manufacturer] = None,
    attributes: Optional[list[Attribute]] = None,
    images: Optional[list[Image]] = None,
) -> Product:
    category = category or await create_category(session)
    country = country or await create_country(session)
    manufacturer = manufacturer or await create_manufacturer(session)

    product = Product(
        title=faker.unique.word(),
        description=faker.text(max_nb_chars=100),
        price=faker.random_int(min=10, max=300),
        stock_quantity=10,
        is_available=True,
        status=faker.random_choice(elements=[v for v in Status]),
        category=category,
        subcategory=subcategory,
        country=country,
        manufacturer=manufacturer,
        images=images or [],
        attributes=attributes or [],
    )

    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
