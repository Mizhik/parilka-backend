from typing import Awaitable, Callable, List
from uuid import UUID
from httpx import AsyncClient
import pytest

from app.schemas.category import CategorySchema
from app.schemas.subcategory import SubCategorySchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_subcategories(
    client: AsyncClient,
):
    res = await client.get("/subcategories")

    m = parse_response(res, List[SubCategorySchema])

    assert isinstance(m, list)


@pytest.mark.asyncio
async def test_create_subcategory(
    client: AsyncClient,
    subcategory_payload: Callable[[UUID], SubCategorySchema],
    created_category: CategorySchema,
):
    payload = subcategory_payload(created_category.id)
    res = await client.post("/subcategories/add", json=payload.model_dump(mode="json"))

    m = parse_response(res, SubCategorySchema)

    assert not isinstance(m, list)
    assert payload.title == m.title
    assert payload.display_title == m.display_title
    assert payload.parent_id == m.parent_id

    categories = await client.get("/subcategories")

    sc = parse_response(categories, List[SubCategorySchema])

    assert any(
        m.id == scr.id
        and m.title == scr.title
        and m.display_title == scr.display_title
        and m.parent_id == scr.parent_id
        for scr in sc
    )


@pytest.mark.asyncio
async def test_create_duplicate_subcategory(
    client: AsyncClient,
    create_subcategory: Callable[[UUID], Awaitable[SubCategorySchema]],
    subcategory_payload: Callable[[UUID], SubCategorySchema],
    created_category: CategorySchema,
):
    pass

