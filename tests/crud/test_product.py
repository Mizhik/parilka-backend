from typing import Awaitable, Callable, List
from httpx import AsyncClient
import pytest

from app.models.models import Category, Country, Manufacturer
from app.schemas.attribute import AttributeCreateSchema
from app.schemas.image import ImageCreateSchema
from app.schemas.product import ProductCreateSchema, ProductDetailsSchema, ProductSchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient):
    res = await client.get("/products")

    m = parse_response(res, List[ProductSchema])

    assert isinstance(m, list)


@pytest.mark.asyncio
async def test_create_product(
    client: AsyncClient,
    product_payload,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
    image_payload: Callable[[bool], ImageCreateSchema],
    attribute_payload: Callable[[], AttributeCreateSchema],
):
    image = image_payload(False)
    attribute = attribute_payload()
    category = await category_factory()
    manufacturer = await manufacturer_factory()
    country = await country_factory()
    product: ProductCreateSchema = product_payload(
        images=[image],
        attributes=[attribute],
        category=category,
        manufacturer=manufacturer,
        country=country,
    )

    res = await client.post("/products/add", json=product.model_dump(mode="json"))

    m = parse_response(res, ProductDetailsSchema)

    # assert m.
