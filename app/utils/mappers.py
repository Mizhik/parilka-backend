from collections import defaultdict
from typing import Dict, List, Union
from app.models.enums import AttributeGroupEnum
from app.models.models import Product
from app.schemas.category import CategorySchema
from app.schemas.product import ProductDetailsSchema, ProductSchema
from app.schemas.image import ImageSchema
from app.schemas.attribute import AttributeSchema
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
    )


def map_product_to_detailed_schema(product: Product) -> ProductDetailsSchema:
    tmp_dict: Dict[AttributeGroupEnum, List[AttributeSchema]] = defaultdict(list)
    for attr in product.attributes:
        tmp_dict[attr.attribute_group].append(AttributeSchema.model_validate(attr))

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
        images=[
            ImageSchema.model_validate(img, from_attributes=True)
            for img in product.images
        ],
        attributes=dict(tmp_dict),
        subcategory_id=product.subcategory_id,
        sub_category=SubCategorySchema.model_validate(product.subcategory)
        if product.subcategory is not None
        else None,
    )
