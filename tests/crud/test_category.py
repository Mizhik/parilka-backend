import asyncio
from typing import Awaitable, Callable, List
from uuid import uuid4
from httpx import AsyncClient
import pytest
from app.routes import categories
from app.schemas.category import CategorySchema
from app.schemas.response import ResponseSchema

@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient, created_category: CategorySchema):
    response = await client.get("/categories")

    assert response.status_code == 200

    m = ResponseSchema[List[CategorySchema]].model_validate(response.json())
    
    assert isinstance(m.data, list)
    assert created_category in m.data

@pytest.mark.asyncio
async def test_create_category(client: AsyncClient, category_payload: Callable[[], CategorySchema]):
    payload: CategorySchema = category_payload()
    response = await client.post("/categories/add", json=payload.model_dump())

    assert response.status_code == 200

    m = ResponseSchema[CategorySchema].model_validate(response.json())
    assert not isinstance(m.data, list)
    assert m.data.title == payload.title

@pytest.mark.asyncio
async def test_create_duplicate_category(client: AsyncClient, created_category: CategorySchema):
    response = await client.post("/categories/add", json={"title": created_category.title})

    assert response.status_code == 409

@pytest.mark.asyncio
async def test_edit_category(client: AsyncClient, created_category: CategorySchema, category_payload: Callable[[], CategorySchema]):
    payload = category_payload()

    response = await client.patch(f"/categories/edit/{created_category.id}", json=payload.model_dump(exclude_none=True))

    assert response.status_code == 200

    m = ResponseSchema[CategorySchema].model_validate(response.json())

    assert not isinstance(m.data, list)
    assert m.data.title != created_category.title
    assert m.data.title == payload.title

@pytest.mark.asyncio
async def test_edit_duplicate_category(client: AsyncClient, create_categories: Callable[[], Awaitable[List[CategorySchema]]]):
    categories: List[CategorySchema] = await create_categories()
    cat1, cat2 = categories
    payload = CategorySchema(title=cat1.title)
    response = await client.patch(f"/categories/edit/{cat2.id}", json=payload.model_dump())

    assert response.status_code == 409

@pytest.mark.asyncio
async def test_edit_not_exists_category(client: AsyncClient, category_payload: Callable[[], CategorySchema]):
    payload: CategorySchema = category_payload()
    random_uuid = uuid4()
    response = await client.patch(f"/categories/edit/{random_uuid}", json=payload.model_dump())

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient, created_category: CategorySchema):
    response = await client.delete(f"/categories/delete/{created_category.id}")

    assert response.status_code == 200

    categories = await client.get("/categories")
    
    m = ResponseSchema[List[CategorySchema]].model_validate(categories.json())

    assert not created_category in m.data

@pytest.mark.asyncio
async def test_delete_not_exists_category(client: AsyncClient):
    random_uuid = uuid4()

    response = await client.delete(f"/categories/delete/{random_uuid}")

    assert response.status_code == 404

