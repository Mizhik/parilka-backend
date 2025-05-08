from typing import Awaitable, Callable, List
from uuid import uuid4
from httpx import AsyncClient
import pytest
from app.schemas.manufacturer import ManufacturerCreateSchema, ManufacturerSchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    res = await client.get("/manufacturers")

    m = parse_response(res, List[ManufacturerSchema])
    assert isinstance(m, list)


@pytest.mark.asyncio
async def test_create_manufacturer(
    client: AsyncClient, manufacturer_payload: Callable[[], ManufacturerCreateSchema]
):
    payload = manufacturer_payload()
    res = await client.post("/manufacturers/add", json=payload.model_dump())

    m = parse_response(res, ManufacturerSchema)

    assert not isinstance(m, list)
    assert m.name == payload.name

    manufacturers = await client.get("/manufacturers")

    mf = parse_response(manufacturers, List[ManufacturerSchema])

    assert any(m.id == mfr.id for mfr in mf)


@pytest.mark.asyncio
async def test_create_duplicate_manufacturer(
    client: AsyncClient, created_manufacturer: ManufacturerSchema
):
    payload = ManufacturerCreateSchema(name=created_manufacturer.name)
    res = await client.post("/manufacturers/add", json=payload.model_dump())
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_edit_manufacturer(
    client: AsyncClient,
    created_manufacturer: ManufacturerSchema,
    manufacturer_payload: Callable[[], ManufacturerCreateSchema],
):
    payload = manufacturer_payload()
    res = await client.patch(
        f"/manufacturers/edit/{created_manufacturer.id}", json=payload.model_dump()
    )
    m = parse_response(res, ManufacturerSchema)

    assert not isinstance(m, list)
    assert m.name != created_manufacturer.name
    assert m.name == payload.name

    manufacturers = await client.get("/manufacturers")

    mf = parse_response(manufacturers, List[ManufacturerSchema])

    assert any(m.id == mfr.id and created_manufacturer.name != mfr.name for mfr in mf)


@pytest.mark.asyncio
async def test_edit_duplicate_manufacturer(
    client: AsyncClient,
    create_manufacturers: Callable[[], Awaitable[List[ManufacturerSchema]]],
):
    manufacturers = await create_manufacturers()
    mn1, mn2 = manufacturers
    res = await client.patch(f"/manufacturers/edit/{mn1.id}", json={"name": mn2.name})

    assert res.status_code == 409


@pytest.mark.asyncio
async def test_edit_non_existent_manufacturer(
    client: AsyncClient, manufacturer_payload: Callable[[], ManufacturerCreateSchema]
):
    payload = manufacturer_payload()
    random_uuid = uuid4()
    res = await client.patch(
        f"/manufacturers/edit/{random_uuid}", json=payload.model_dump()
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_manufacturer(
    client: AsyncClient, created_manufacturer: ManufacturerSchema
):
    res = await client.delete(f"/manufacturers/delete/{created_manufacturer.id}")

    assert res.status_code == 200

    manufacturers = await client.get("/manufacturers")

    m = parse_response(manufacturers, List[ManufacturerSchema])

    assert any(created_manufacturer.id != mfr.id for mfr in m)


@pytest.mark.asyncio
async def test_delete_non_existent_manufacturer(client: AsyncClient):
    random_uuid = uuid4()

    res = await client.delete(f"/manufacturers/delete/{random_uuid}")

    assert res.status_code == 404
