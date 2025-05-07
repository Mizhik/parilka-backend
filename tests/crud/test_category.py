from httpx import AsyncClient
import pytest
from app.schemas.category import CategorySchema

import logging

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    payload = {"title": "Test"}

    response = await client.post("/categories/add", json=payload)

    assert response.status_code == 200

    m = CategorySchema.model_validate(response.json()["data"])

    assert m.title == "Test"
