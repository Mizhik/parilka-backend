# type: ignore
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.base_model import Base
from app.database.db import get_db
from app.core.settings import Settings
from httpx import ASGITransport, AsyncClient
from asgi import app as fastapi_app

TEST_DATABASE_URL = Settings().ASYNC_TEST_DATABASE_URL

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)


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


# @pytest_asyncio.fixture(autouse=True)
# async def bind_factories(db_session: AsyncSession):
#     ProductFactory._meta.sqlalchemy_session = db_session
#     CategoryFactory._meta.sqlalchemy_session = db_session
# Add other factories here as needed
