from app.schemas.product import ProductSchema
from app.schemas.image import ImageSchema
from app.schemas.attribute import AttributeSchema


def map_product_to_schema(product) -> ProductSchema:
    return ProductSchema(
        id=product.id,
        title=product.title,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        is_available=product.is_available,
        is_popular=product.is_popular,
        is_new=product.is_new,
        category_id=product.category_id,
        country_of_origin_id=product.country_of_origin_id,
        manufacturer_id=product.manufacturer_id,
        images=[ImageSchema.model_validate(img, from_attributes=True) for img in product.images],
        attributes=[AttributeSchema.model_validate(attr, from_attributes=True) for attr in product.attributes],
    )
