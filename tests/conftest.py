from decimal import Decimal
from enum import auto
from asgi_lifespan import LifespanManager
from typing import Awaitable, Callable, Generator, List
import asyncio
from uuid import UUID
import faker as faker_
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.base_model import Base
from app.database.db import get_db
from app.core.settings import Settings
from httpx import ASGITransport, AsyncClient
from app.models.enums import AttributeGroupEnum, ProductStatus, Status
from app.models.models import (
    BundleContent,
    Category,
    Country,
    Manufacturer,
    SubCategory,
)
from app.schemas.attribute import AttributeCreateSchema
from app.schemas.bundle import BundleCreateSchema
from app.schemas.category import CategoryCreateSchema
from app.schemas.country import CountryCreateSchema
from app.schemas.image import ImageCreateSchema, ImageSchema
from app.schemas.manufacturer import ManufacturerCreateSchema
from app.schemas.product import ProductCreateSchema
from app.schemas.subcategory import SubCategoryCreateSchema
from asgi import app as fastapi_app
import pytest

from tests.factories.category import create_category
from tests.factories.country import create_country
from tests.factories.manufacturer import create_manufacturer
from tests.factories.product import create_product
from tests.factories.subcategory import create_subcategory
from tests.utils import bulk_creator, bulk_creator_with_args

TEST_DATABASE_URL = Settings().ASYNC_TEST_DATABASE_URL


faker = faker_.Faker()


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine):
    connection = await test_engine.connect()
    transaction = await connection.begin()

    AsyncSessionLocal = async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()
            await connection.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    async with LifespanManager(fastapi_app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as client:
            yield client
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def category_payload() -> Callable[[], CategoryCreateSchema]:
    def _create_payload():
        return CategoryCreateSchema(title=faker.word())

    return _create_payload


@pytest.fixture(scope="function")
def manufacturer_payload() -> Callable[[], ManufacturerCreateSchema]:
    def _create_payload():
        return ManufacturerCreateSchema(name=faker.company())

    return _create_payload


@pytest.fixture(scope="function")
def country_payload() -> Callable[[], CountryCreateSchema]:
    def _create_payload():
        return CountryCreateSchema(name=faker.country())

    return _create_payload


@pytest.fixture(scope="function")
def subcategory_payload() -> Callable[[UUID], SubCategoryCreateSchema]:
    def _create_payload(parent_id: UUID):
        return SubCategoryCreateSchema(
            title=faker.word(),
            display_title=faker.word(),
            parent_id=parent_id,
        )

    return _create_payload


@pytest.fixture(scope="function")
def image_payload():
    def _create_payload(is_main: bool):
        return ImageCreateSchema(image_url=faker.word(), is_main=is_main)

    return _create_payload


@pytest.fixture(scope="function")
def attribute_payload():
    def _create_payload(images: List[ImageCreateSchema]):
        return AttributeCreateSchema(
            attribute_group=faker.random_element(
                elements=[v for v in AttributeGroupEnum]
            ),  # type: ignore
            value=faker.unique.word(),
            price_modifier=None,
            stock_quantity=faker.random_int(min=1, max=10),
            images=[*images],
        )

    return _create_payload


@pytest.fixture(scope="function")
def product_payload():
    def _create_payload(
        category: Category,
        country: Country,
        manufacturer: Manufacturer,
        images: List[ImageCreateSchema],
        attributes: List[AttributeCreateSchema],
        bundle_items: List[BundleCreateSchema] = [],
    ):
        return ProductCreateSchema(
            title=faker.word(),
            attributes=attributes,
            category_id=category.id,
            country_of_origin_id=country.id,
            description=faker.word(),
            discount_price=None,
            images=images,
            is_available=True,
            manufacturer_id=manufacturer.id,
            price=Decimal("20.5"),
            status=faker.random_element(elements=[v for v in ProductStatus]),  # type: ignore
            stock_quantity=faker.random_int(min=2, max=30),
            subcategory_id=None,
            bundle_items=bundle_items,
        )

    return _create_payload


@pytest.fixture(scope="function")
def manufacturer_factory(db_session: AsyncSession):
    return lambda: create_manufacturer(db_session)


@pytest.fixture(scope="function")
def create_manufacturers(manufacturer_factory: Callable[[], Awaitable[Manufacturer]]):
    return bulk_creator(manufacturer_factory)


@pytest.fixture(scope="function")
def country_factory(db_session: AsyncSession):
    return lambda: create_country(db_session)


@pytest.fixture(scope="function")
def create_countries(country_factory: Callable[[], Awaitable[Country]]):
    return bulk_creator(country_factory)


@pytest.fixture(scope="function")
def category_factory(db_session: AsyncSession):
    return lambda: create_category(db_session)


@pytest.fixture(scope="function")
def create_categories(category_factory: Callable[[], Awaitable[Category]]):
    return bulk_creator(category_factory)


@pytest.fixture(scope="function")
def subcategory_factory(db_session: AsyncSession):
    return lambda category: create_subcategory(db_session, category)


@pytest.fixture(scope="function")
def create_subcategories(
    subcategory_factory: Callable[[List[Category]], Awaitable[SubCategory]],
):
    return bulk_creator_with_args(subcategory_factory)


@pytest.fixture(scope="function")
def product_factory(db_session: AsyncSession):
    return lambda category, images, attributes, manufacturer, country: create_product(
        db_session,
        manufacturer=manufacturer,
        category=category,
        images=images,
        attributes=attributes,
        country=country,
    )
