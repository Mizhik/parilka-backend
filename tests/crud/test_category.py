from typing import Awaitable, Callable, List
from uuid import uuid4
from httpx import AsyncClient
import pytest
from app.models.models import Category
from app.schemas.category import CategoryCreateSchema, CategorySchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    response = await client.get("/categories")

    m = parse_response(response, List[CategorySchema])

    assert isinstance(m, list)


@pytest.mark.asyncio
async def test_create_category(
    client: AsyncClient, category_payload: Callable[[], CategoryCreateSchema]
):
    payload = category_payload()
    response = await client.post("/categories/add", json=payload.model_dump())
    m = parse_response(response, CategorySchema)
    assert not isinstance(m, list)
    assert m.title == payload.title

    categories = await client.get("/categories")

    c = parse_response(categories, List[CategorySchema])

    assert any(m.id == ct.id for ct in c)


@pytest.mark.asyncio
async def test_create_duplicate_category(
    client: AsyncClient, category_factory: Callable[[], Awaitable[CategorySchema]]
):
    category = await category_factory()
    response = await client.post(
        "/categories/add", json={"title": category.title}
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_edit_category(
    client: AsyncClient,
    category_factory: Callable[[], Awaitable[Category]],
    category_payload: Callable[[], CategoryCreateSchema],
):
    payload = category_payload()

    category = await category_factory()
    original_title = category.title

    response = await client.patch(
        f"/categories/edit/{category.id}",
        json=payload.model_dump(),
    )

    m = parse_response(response, CategorySchema)

    assert not isinstance(m, list)
    assert m.title != original_title
    assert m.title == payload.title

    categories = await client.get("/categories")

    c = parse_response(categories, List[CategorySchema])

    assert any(m.id == ct.id and original_title != ct.title for ct in c), "Edited category not present in GET categories"


@pytest.mark.asyncio
async def test_edit_duplicate_category(
    client: AsyncClient,
    create_categories: Callable[[], Awaitable[List[CategorySchema]]],
):
    categories: List[CategorySchema] = await create_categories()
    cat1, cat2 = categories
    payload = CategoryCreateSchema(title=cat1.title)
    response = await client.patch(
        f"/categories/edit/{cat2.id}", json=payload.model_dump()
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_edit_not_exists_category(
    client: AsyncClient, category_payload: Callable[[], CategoryCreateSchema]
):
    payload = category_payload()
    random_uuid = uuid4()
    response = await client.patch(
        f"/categories/edit/{random_uuid}", json=payload.model_dump()
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient, category_factory: Callable[[], Awaitable[Category]]):
    category = await category_factory()
    response = await client.delete(f"/categories/delete/{category.id}")

    assert response.status_code == 200

    categories = await client.get("/categories")

    m = parse_response(categories, List[CategorySchema])

    assert any(ct.id != category.id for ct in m)


@pytest.mark.asyncio
async def test_delete_not_exists_category(client: AsyncClient):
    random_uuid = uuid4()

    response = await client.delete(f"/categories/delete/{random_uuid}")

    assert response.status_code == 404
