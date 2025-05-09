from typing import Awaitable, Callable, Generator
import asyncio
from uuid import UUID
import faker as faker_
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.base_model import Base
from app.database.db import get_db
from app.core.settings import Settings
from httpx import ASGITransport, AsyncClient
from app.models.models import Category, Country, Manufacturer, SubCategory
from app.schemas.category import CategoryCreateSchema
from app.schemas.country import CountryCreateSchema
from app.schemas.manufacturer import ManufacturerCreateSchema
from app.schemas.subcategory import SubCategoryCreateSchema
from asgi import app as fastapi_app
import pytest

from tests.factories.category import create_category
from tests.factories.country import create_country
from tests.factories.manufacturer import create_manufacturer
from tests.factories.subcategory import create_subcategory
from tests.utils import bulk_creator, bulk_creator_with_args

TEST_DATABASE_URL = Settings().ASYNC_TEST_DATABASE_URL

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

faker = faker_.Faker()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
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


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as client:
        yield client
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def category_payload() -> Callable[[], CategoryCreateSchema]:
    def _create_payload():
        return CategoryCreateSchema(title=faker.word())

    return _create_payload


# @pytest.fixture(scope="function")
# def create_category(
#     client: AsyncClient, category_payload: Callable[[], CategorySchema]
# ):
#     async def _create():
#         payload = category_payload()
#         response = await client.post("/categories/add", json=payload.model_dump())
#         return CategorySchema.model_validate(response.json()["data"])
#     return _create


# @pytest.fixture(scope="function")
# def create_categories(client: AsyncClient, category_payload):
#     async def _create_multiple(count=2):
#         categories = []
#         for _ in range(count):
#             payload = category_payload()
#             response = await client.post("/categories/add", json=payload.model_dump())
#             category = CategorySchema.model_validate(response.json()["data"])
#             categories.append(category)
#         return categories
#
#     return _create_multiple


@pytest.fixture(scope="function")
def manufacturer_payload() -> Callable[[], ManufacturerCreateSchema]:
    def _create_payload():
        return ManufacturerCreateSchema(name=faker.company())

    return _create_payload


# @pytest.fixture(scope="function")
# def create_manufacturer(
#     client: AsyncClient, manufacturer_payload: Callable[[], ManufacturerCreateSchema]
# ):
#     async def _create():
#         payload = manufacturer_payload()
#         response = await client.post("/manufacturers/add", json=payload.model_dump())
#         return ManufacturerSchema.model_validate(response.json()["data"])
#     return _create


# @pytest.fixture(scope="function")
# def create_manufacturers(
#     client: AsyncClient, manufacturer_payload: Callable[[], ManufacturerCreateSchema]
# ):
#     async def _create_multiple(count=2):
#         manufacturers = []
#         for _ in range(count):
#             payload = manufacturer_payload()
#             response = await client.post(
#                 "/manufacturers/add", json=payload.model_dump()
#             )
#             manufacturer = ManufacturerSchema.model_validate(response.json()["data"])
#             manufacturers.append(manufacturer)
#         return manufacturers
#
#     return _create_multiple


@pytest.fixture(scope="function")
def country_payload() -> Callable[[], CountryCreateSchema]:
    def _create_payload():
        return CountryCreateSchema(name=faker.country())

    return _create_payload


# @pytest.fixture(scope="function")
# def create_country(
#     client: AsyncClient, country_payload: Callable[[], CountryCreateSchema]
# ):
#     async def _create():
#         payload = country_payload()
#         response = await client.post("/countries/add", json=payload.model_dump())
#         return CountrySchema.model_validate(response.json()["data"])
#     return _create



@pytest.fixture(scope="function")
def subcategory_payload() -> Callable[[UUID], SubCategoryCreateSchema]:
    def _create_payload(parent_id: UUID):
        return SubCategoryCreateSchema(
            title=faker.word(),
            display_title=faker.word(),
            parent_id=parent_id,
        )

    return _create_payload


# @pytest.fixture(scope="function")
# def create_subcategory(
#     client: AsyncClient,
#     subcategory_payload: Callable[[UUID], SubCategoryCreateSchema],
# ):
#     async def _create(category_id: UUID):
#         payload = subcategory_payload(category_id)
#         response = await client.post(
#             "/subcategories/add", json=payload.model_dump(mode="json")
#         )
#         return SubCategorySchema.model_validate(response.json()["data"])
#
#     return _create
#

# @pytest.fixture(scope="function")
# def create_subcategories(
#     client: AsyncClient,
#     subcategory_payload: Callable[[UUID], SubCategoryCreateSchema],
# ):
#     async def _create_multiple(categories: List[CategorySchema]):
#         subcats = []
#         for idx in range(len(categories)):
#             payload = subcategory_payload(categories[idx].id)
#             response = await client.post(
#                 "/subcategories/add", json=payload.model_dump()
#             )
#             subcat = SubCategorySchema.model_validate(response.json()["data"])
#             subcats.append(subcat)
#         return subcats
#
#     return _create_multiple


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
def create_subcategories(subcategory_factory: Callable[[Category], Awaitable[SubCategory]]):
    return bulk_creator_with_args(subcategory_factory)
