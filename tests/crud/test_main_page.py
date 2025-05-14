import pytest
from httpx import AsyncClient

from app.models.enums import ProductStatus
from app.schemas.main_page import MainPageSchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_main_page(client: AsyncClient):
    main_page = await client.get("/main-page")

    m = parse_response(main_page, MainPageSchema)

    assert all(pr.status == ProductStatus.DISCOUNT for pr in m.discounts)
    assert all(pr.status == ProductStatus.POPULAR for pr in m.popular)
    assert all(pr.status == ProductStatus.NONE for pr in m.catalogue)
    assert not len(m.discounts) > 4, "Too many results in discounts"
    assert not len(m.catalogue) > 4, "Too many results in catalogue"
    assert not len(m.popular) > 4, "Too many results in popular"
