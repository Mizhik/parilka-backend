

from typing import Awaitable, Callable, List
from uuid import uuid4
from httpx import AsyncClient
import pytest
from app.schemas.manufacturer import ManufacturerCreateSchema, ManufacturerSchema
from app.schemas.response import ResponseSchema
from tests.conftest import created_manufacturer


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient, created_manufacturer: ManufacturerSchema):
    res = await client.get("/manufacturers")

    assert res.status_code == 200

    m = ResponseSchema[List[ManufacturerSchema]].model_validate(res.json())
    
    assert isinstance(m.data, list)
    assert created_manufacturer in m.data

@pytest.mark.asyncio
async def test_create_duplicate_manufacturer(client: AsyncClient, created_manufacturer: ManufacturerSchema):
    payload = ManufacturerCreateSchema(name=created_manufacturer.name)
    res = await client.post("/manufacturers/add", json=payload.model_dump())
    assert res.status_code == 409

@pytest.mark.asyncio
async def test_edit_manufacturer(client: AsyncClient, created_manufacturer: ManufacturerSchema, manufacturer_payload: Callable[[], ManufacturerCreateSchema]):
    payload = manufacturer_payload()
    res = await client.patch(f"/manufacturers/edit/{created_manufacturer.id}", json=payload.model_dump())
    
    assert res.status_code == 200

    m = ResponseSchema[ManufacturerSchema].model_validate(res.json())

    assert not isinstance(m.data, list)
    assert m.data.name != created_manufacturer.name
    assert m.data.name == payload.name

@pytest.mark.asyncio
async def test_edit_duplicate_manufacturer(client: AsyncClient, create_manufacturers: Callable[[], Awaitable[List[ManufacturerSchema]]]):
    manufacturers = await create_manufacturers()
    mn1, mn2 = manufacturers
    res = await client.patch(f"/manufacturers/edit/{mn1.id}", json={"name": mn2.name})

    assert res.status_code == 409
    
@pytest.mark.asyncio
async def test_edit_non_existent_manufacturer(client: AsyncClient, manufacturer_payload: Callable[[], ManufacturerCreateSchema]):
    payload = manufacturer_payload()
    random_uuid = uuid4()
    res = await client.patch(f"/manufacturers/edit/{random_uuid}", json=payload.model_dump())

    assert res.status_code == 404

@pytest.mark.asyncio
async def test_delete_manufacturer(client: AsyncClient, created_manufacturer: ManufacturerSchema):
    res = await client.delete(f"/manufacturers/delete/{created_manufacturer.id}")

    assert res.status_code == 200

    mn = await client.get("/manufacturers")

    assert mn.status_code == 200

    m = ResponseSchema[List[ManufacturerSchema]].model_validate(mn.json())

    assert not created_manufacturer in m.data

@pytest.mark.asyncio
async def test_delete_non_existent_manufacturer(client: AsyncClient):
    random_uuid = uuid4()

    res = await client.delete(f"/manufacturers/delete/{random_uuid}")

    assert res.status_code == 404
