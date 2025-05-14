from typing import Awaitable, Callable, List
from uuid import UUID, uuid4
from httpx import AsyncClient
import pytest
import faker as faker_

from app.models.models import Category, SubCategory
from app.schemas.category import CategorySchema
from app.schemas.subcategory import SubCategorySchema
from tests.utils import parse_response

faker = faker_.Faker()


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
    category_factory: Callable[[], Awaitable[CategorySchema]],
):
    category = await category_factory()
    payload = subcategory_payload(category.id)
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
async def test_create_non_existent_parent_subcategory(
    client: AsyncClient,
    subcategory_payload: Callable[[UUID], SubCategorySchema],
):
    random_uuid = uuid4()
    payload = subcategory_payload(random_uuid)

    res = await client.post("/subcategories/add", json=payload.model_dump(mode="json"))

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate_subcategory(
    client: AsyncClient,
    subcategory_factory: Callable[[Category], Awaitable[SubCategorySchema]],
    subcategory_payload: Callable[[UUID], SubCategorySchema],
    category_factory: Callable[[], Awaitable[Category]],
):
    category = await category_factory()
    subcategory = await subcategory_factory(category)
    new_subcategory = subcategory_payload(category.id)
    new_subcategory.title = subcategory.title

    res = await client.post(
        "/subcategories/add", json=new_subcategory.model_dump(mode="json")
    )

    assert res.status_code == 409, "Subcategory with the same title added"

    new_subcategory2 = subcategory_payload(category.id)
    new_subcategory2.display_title = subcategory.display_title

    res2 = await client.post(
        "/subcategories/add", json=new_subcategory2.model_dump(mode="json")
    )
    assert res2.status_code == 409, "Subcategory with the same display title added"


@pytest.mark.asyncio
async def test_edit_subcategory(
    client: AsyncClient,
    subcategory_factory: Callable[[Category], Awaitable[SubCategorySchema]],
    category_factory: Callable[[], Awaitable[Category]],
):
    category = await category_factory()
    subcategory = await subcategory_factory(category)
    original_title = subcategory.title
    original_display_title = subcategory.display_title
    payload = {"title": faker.word(), "display_title": faker.word()}

    res = await client.patch(f"/subcategories/edit/{subcategory.id}", json=payload)

    m = parse_response(res, SubCategorySchema)

    assert not isinstance(m, list)
    assert payload["title"] == m.title
    assert payload["display_title"] == m.display_title
    assert m.title != original_title
    assert m.display_title != original_display_title

    subcategories = await client.get("/subcategories")

    sc = parse_response(subcategories, List[SubCategorySchema])

    assert any(
        m.id == scr.id
        and m.title == scr.title
        and m.display_title == scr.display_title
        and m.parent_id == scr.parent_id
        for scr in sc
    )


@pytest.mark.asyncio
async def test_edit_duplicate_subcategory(
    client: AsyncClient,
    create_subcategories: Callable[[List[Category]], Awaitable[List[SubCategory]]],
    create_categories: Callable[[], Awaitable[List[Category]]],
):
    categories = await create_categories()
    subcategories = await create_subcategories(categories)

    sub1, sub2 = subcategories

    payload = {"title": sub2.title}

    res = await client.patch(f"/subcategories/edit/{sub1.id}", json=payload)

    assert res.status_code == 409

    payload2 = {"display_title": sub2.display_title}

    res2 = await client.patch(f"/subcategories/edit/{sub1.id}", json=payload2)

    assert res2.status_code == 409


@pytest.mark.asyncio
async def test_edit_non_existent_parent_subcategory(
    client: AsyncClient, subcategory_payload: Callable[[UUID], SubCategorySchema]
):
    random_uuid = uuid4()
    subcategory = subcategory_payload(random_uuid)

    res = await client.patch(
        f"/subcategories/edit/{random_uuid}", json=subcategory.model_dump(mode="json")
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_subcategory(
    client: AsyncClient,
    category_factory: Callable[[], Awaitable[Category]],
    subcategory_factory: Callable[[Category], Awaitable[SubCategory]],
):
    category = await category_factory()
    subcategory = await subcategory_factory(category)

    res = await client.delete(f"/subcategories/delete/{subcategory.id}")

    assert res.status_code == 200

    subcategories = await client.get("/subcategories")

    sc = parse_response(subcategories, List[SubCategorySchema])

    assert not any(subcategory.id == scr.id for scr in sc)


@pytest.mark.asyncio
async def test_delete_non_existend_subcategory(
    client: AsyncClient,
):
    random_uuid = uuid4()

    res = await client.delete(f"/subcategories/delete/{random_uuid}")

    assert res.status_code == 404
