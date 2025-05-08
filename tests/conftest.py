# type: ignore
from typing import Generator
import asyncio
import faker
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.base_model import Base
from app.database.db import get_db
from app.core.settings import Settings
from httpx import ASGITransport, AsyncClient
from app.schemas.category import CategorySchema
from app.schemas.response import ResponseSchema
from asgi import app as fastapi_app
import pytest

TEST_DATABASE_URL = Settings().ASYNC_TEST_DATABASE_URL

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
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
def category_payload() -> CategorySchema:
    def _create_payload():
        return CategorySchema(title=faker.Faker().word())
    return _create_payload


@pytest_asyncio.fixture(scope="function")
async def created_category(client: AsyncClient, category_payload: CategorySchema) -> CategorySchema:
    payload = category_payload()
    response = await client.post("/categories/add", json=payload.model_dump())
    assert response.status_code == 200
    category = ResponseSchema[CategorySchema].model_validate(response.json())
    assert not isinstance(category.data, list)
    return category.data

@pytest_asyncio.fixture(scope="function")
async def create_categories(client: AsyncClient, category_payload):
    async def _create_multiple(count=2):
        categories = []
        for _ in range(count):
            payload = category_payload()
            response = await client.post("/categories/add", json=payload.model_dump())
            assert response.status_code == 200
            category = ResponseSchema[CategorySchema].model_validate(response.json())
            assert not isinstance(category.data, list)
            categories.append(category.data)
        return categories
    return _create_multiple
