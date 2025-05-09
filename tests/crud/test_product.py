from typing import Awaitable, Callable, List
from httpx import AsyncClient
from pydantic import ValidationError
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
    attribute_payload: Callable[[List[ImageCreateSchema]], AttributeCreateSchema],
):
    image = image_payload(False)
    attribute = attribute_payload([])
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

    assert m.attributes, "Attributes are empty"
    assert len(m.images) > 0, "Images are empty"
    assert m.category is not None

    products = await client.get(f"/products/{m.id}")

    pr = parse_response(products, ProductDetailsSchema)

    assert pr.attributes, "Attributes are empty in get_one"
    assert len(pr.images) > 0, "Images are empty in get_one"
    assert pr.category is not None


@pytest.mark.asyncio
async def test_create_product_main_photo(
    client: AsyncClient,
    product_payload,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
    image_payload: Callable[[bool], ImageCreateSchema],
    attribute_payload: Callable[[List[ImageCreateSchema]], AttributeCreateSchema],
):
    image = image_payload(True)
    attribute = attribute_payload([])
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

    assert m.attributes, "Attributes are empty"
    assert len(m.images) > 0, "Images are empty"
    assert m.category is not None

    products = await client.get("/products")

    pr = parse_response(products, List[ProductSchema])

    assert any(prd.id == m.id and prd.main_image for prd in pr)


@pytest.mark.asyncio
async def test_create_product_main_photo_from_attribute(
    client: AsyncClient,
    product_payload,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
    image_payload: Callable[[bool], ImageCreateSchema],
    attribute_payload: Callable[[List[ImageCreateSchema]], AttributeCreateSchema],
):
    image = image_payload(True)
    attribute = attribute_payload([image])
    category = await category_factory()
    manufacturer = await manufacturer_factory()
    country = await country_factory()
    product: ProductCreateSchema = product_payload(
        images=[],
        attributes=[attribute],
        category=category,
        manufacturer=manufacturer,
        country=country,
    )

    res = await client.post("/products/add", json=product.model_dump(mode="json"))

    m = parse_response(res, ProductDetailsSchema)

    products = await client.get("/products")

    pr = parse_response(products, List[ProductSchema])

    assert any(prd.id == m.id and prd.main_image for prd in pr)


@pytest.mark.asyncio
async def test_create_product_attributes(
    client: AsyncClient,
    product_payload,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
    image_payload: Callable[[bool], ImageCreateSchema],
    attribute_payload: Callable[[List[ImageCreateSchema]], AttributeCreateSchema],
):
    image = image_payload(True)
    attribute = attribute_payload([image])
    attribute2 = attribute_payload([])
    category = await category_factory()
    manufacturer = await manufacturer_factory()
    country = await country_factory()
    product: ProductCreateSchema = product_payload(
        images=[],
        attributes=[attribute, attribute2],
        category=category,
        manufacturer=manufacturer,
        country=country,
    )

    res = await client.post("/products/add", json=product.model_dump(mode="json"))
    m = parse_response(res, ProductDetailsSchema)

    assert m.attributes, "Attributes are empty"
    assert len(m.attributes) == 2, f"Attribute count mismatch {len(m.attributes)}"
    _, attrs = next(iter(m.attributes.items()))
    assert attrs[0].images, "Attribute images are empty"


@pytest.mark.asyncio
async def test_create_product_multiple_main_photos(
    product_payload,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
    image_payload: Callable[[bool], ImageCreateSchema],
    attribute_payload: Callable[[List[ImageCreateSchema]], AttributeCreateSchema],
):
    image = image_payload(True)
    image2 = image_payload(True)
    attribute = attribute_payload([])
    category = await category_factory()
    manufacturer = await manufacturer_factory()
    country = await country_factory()

    with pytest.raises(ValidationError) as excinfo:
        product: ProductCreateSchema = product_payload(
            images=[image, image2],
            attributes=[attribute],
            category=category,
            manufacturer=manufacturer,
            country=country,
        )
    assert "Product can only have 1 main image" in str(excinfo.value)
