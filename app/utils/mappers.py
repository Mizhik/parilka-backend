from collections import defaultdict
from typing import Dict, List
from app.models.enums import AttributeGroupEnum
from app.models.models import Product
from app.schemas.category import CategorySchema
from app.schemas.product import ProductDetailsSchema, ProductSchema
from app.schemas.image import ImageSchema
from app.schemas.attribute import AttributeProductSchema
from app.schemas.subcategory import SubCategorySchema


def map_product_to_schema(product: Product) -> ProductSchema:
    main_image = next(
        (ImageSchema.model_validate(img) for img in product.images if img.is_main), None
    )
    if main_image is None:
        for attribute in product.attributes:
            if main_image is not None:
                break
            main_image = next(
                (
                    ImageSchema.model_validate(img)
                    for img in attribute.images
                    if img.is_main
                ),
                None,
            )
    return ProductSchema(
        id=product.id,
        title=product.title,
        price=product.price,  # type: ignore
        main_image=main_image,
        status=product.status,
    )


# TODO: Quantity should be calculated from attributes, if there are any
def map_product_to_detailed_schema(product: Product) -> ProductDetailsSchema:
    bundle_items = [
        map_product_to_schema(bundle.product) for bundle in product.bundle_items
    ]
    images = [ImageSchema.model_validate(img) for img in product.images] + [
        ImageSchema.model_validate(img)
        for attr in product.attributes
        for img in (attr.images or [])
    ]
    tmp_dict: Dict[AttributeGroupEnum, List[AttributeProductSchema]] = defaultdict(list)
    for attr in product.attributes:
        tmp_dict[attr.attribute_group].append(
            AttributeProductSchema.model_validate(attr)
        )

    return ProductDetailsSchema(
        id=product.id,
        title=product.title,
        price=product.price,  # type: ignore
        description=product.description,
        category=CategorySchema.model_validate(product.category),
        is_available=product.is_available,
        stock_quantity=product.stock_quantity,
        status=product.status,
        country_of_origin_id=product.country_of_origin_id,
        manufacturer_id=product.manufacturer_id,
        images=images,
        attributes=dict(tmp_dict),
        bundle_items=bundle_items,
        subcategory_id=product.subcategory_id,
        sub_category=SubCategorySchema.model_validate(product.subcategory)
        if product.subcategory is not None
        else None,
    )
