from typing import Awaitable, Callable, List
from uuid import uuid4
from httpx import AsyncClient
import pytest

from app.schemas.country import CountryCreateSchema, CountrySchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_countries(client: AsyncClient):
    res = await client.get("/countries")

    m = parse_response(res, List[CountrySchema])

    assert isinstance(m, list)


@pytest.mark.asyncio
async def test_create_country(
    client: AsyncClient, country_payload: Callable[[], CountryCreateSchema]
):
    payload = country_payload()

    res = await client.post("/countries/add", json=payload.model_dump())

    m = parse_response(res, CountrySchema)

    assert not isinstance(m, list)
    assert m.name == payload.name

    countries = await client.get("/countries")

    c = parse_response(countries, List[CountrySchema])

    assert any(m.id == ct.id and m.name == ct.name for ct in c)


@pytest.mark.asyncio
async def test_create_duplicate_country(
    client: AsyncClient, created_country: CountrySchema
):
    res = await client.post("/countries/add", json={"name": created_country.name})

    assert res.status_code == 409


@pytest.mark.asyncio
async def test_edit_category(
    client: AsyncClient,
    created_country: CountrySchema,
    country_payload: Callable[[], CountryCreateSchema],
):
    payload = country_payload()
    res = await client.patch(
        f"/countries/edit/{created_country.id}", json=payload.model_dump()
    )

    m = parse_response(res, CountrySchema)
    assert not isinstance(m, list)
    assert created_country.name != m.name
    assert m.name == payload.name

    countries = await client.get("/countries")

    c = parse_response(countries, List[CountrySchema])

    assert isinstance(c, list)
    assert any(ct.id == m.id and ct.name == payload.name for ct in c)


@pytest.mark.asyncio
async def test_edit_duplicate_country(
    client: AsyncClient, create_countries: Callable[[], Awaitable[List[CountrySchema]]]
):
    countries = await create_countries()
    c1, c2 = countries
    res = await client.patch(f"/countries/edit/{c1.id}", json={"name": c2.name})

    assert res.status_code == 409


@pytest.mark.asyncio
async def test_edit_non_existent(
    client: AsyncClient, country_payload: Callable[[], CountryCreateSchema]
):
    payload = country_payload()
    random_uuid = uuid4()
    res = await client.patch(
        f"/countries/edit/{random_uuid}", json=payload.model_dump()
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_country(client: AsyncClient, created_country: CountrySchema):
    res = await client.delete(f"/countries/delete/{created_country.id}")
    assert res.status_code == 200

    countries = await client.get("/countries")

    m = parse_response(countries, List[CountrySchema])

    assert any(created_country.id != ct.id for ct in m)


@pytest.mark.asyncio
async def test_delete_non_existent_country(client: AsyncClient):
    random_uuid = uuid4()
    res = await client.delete(f"/countries/delete/{random_uuid}")
    assert res.status_code == 404
