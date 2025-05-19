from decimal import Decimal
from typing import Awaitable, Callable, List
from httpx import AsyncClient
from pydantic import ValidationError
import pytest
from sqlalchemy import literal

from app.models.models import Category, Country, Manufacturer, Product
from app.schemas.attribute import AttributeCreateSchema
from app.schemas.bundle import BundleCreateSchema
from app.schemas.image import ImageCreateSchema
from app.schemas.product import ProductCreateSchema, ProductDetailsSchema, ProductSchema
from tests.utils import parse_response


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient):
    res = await client.get("/products")

    parse_response(res, List[ProductSchema])


@pytest.mark.asyncio
async def test_get_similar(
    client: AsyncClient,
    product_factory,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
):
    category = await category_factory()
    manufacturer = await manufacturer_factory()
    country = await country_factory()
    product: Product = await product_factory(category, [], [], manufacturer, country)
    for _ in range(10):
        c = await category_factory()
        m = await manufacturer_factory()
        ct = await country_factory()
        await product_factory(c, [], [], m, ct)

    res = await client.get(f"/products/{product.id}/similar")

    sp = parse_response(res, List[ProductSchema])

    assert not any(p.price > (product.price * Decimal("1.12")) for p in sp), (  # type: ignore
        "Got expensive product"
    )
    assert not any(p.price < (product.price * Decimal("0.8")) for p in sp), (  # type: ignore
        "Got cheap product"
    )


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

    products = await client.get(f"/products/{m.sku}")

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
    attributes = [attribute, attribute2]
    product: ProductCreateSchema = product_payload(
        images=[],
        attributes=attributes,
        category=category,
        manufacturer=manufacturer,
        country=country,
    )

    res = await client.post("/products/add", json=product.model_dump(mode="json"))
    m = parse_response(res, ProductDetailsSchema)

    assert m.attributes, "Attributes are empty"
    expected_keys = set()
    for attr in [attribute, attribute2]:
        if hasattr(attr, "attribute_group"):
            expected_keys.add(attr.attribute_group)

    actual_keys = set(m.attributes.keys()) if isinstance(m.attributes, dict) else set()
    assert actual_keys == expected_keys, (
        f"Attribute keys mismatch. \n Expected: {expected_keys} \n Got: {actual_keys}. Request sent as: {product.attributes}"
    )
    assert m.images, "Images are missing from attributes"


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
        product_payload(
            images=[image, image2],
            attributes=[attribute],
            category=category,
            manufacturer=manufacturer,
            country=country,
        )
        assert "Product can only have 1 main image" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_product_bundle(
    client: AsyncClient,
    product_payload,
    product_factory,
    manufacturer_factory: Callable[[], Awaitable[Manufacturer]],
    category_factory: Callable[[], Awaitable[Category]],
    country_factory: Callable[[], Awaitable[Country]],
):
    category = await category_factory()
    manufacturer = await manufacturer_factory()
    country = await country_factory()
    created_product: Product = await product_factory(
        category, [], [], manufacturer, country
    )
    bundle_item = BundleCreateSchema(product_id=created_product.id)
    product: ProductCreateSchema = product_payload(
        images=[],
        attributes=[],
        manufacturer=manufacturer,
        category=category,
        country=country,
        bundle_items=[bundle_item],
    )

    res = await client.post("/products/add", json=product.model_dump(mode="json"))

    m = parse_response(res, ProductDetailsSchema)

    assert m.bundle_items, "No bundle items"
    assert any(created_product.id == b.id for b in m.bundle_items)
