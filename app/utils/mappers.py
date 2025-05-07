from app.models.models import Product
from app.schemas.product import ProductDetailsSchema, ProductSchema
from app.schemas.image import ImageSchema
from app.schemas.attribute import AttributeSchema


def map_product_to_schema(product: Product, is_full: bool = False) -> ProductSchema:
    if not is_full:
        main_image = next((ImageSchema.model_validate(img) for img in product.images if img.is_main), None)
        if main_image is None:
            for attribute in product.attributes:
                if main_image is not None: 
                    break
                main_image = next((ImageSchema.model_validate(img) for img in attribute.images if img.is_main), None)
        return ProductSchema(
            id=product.id,
            title=product.title,
            price=product.price, # type: ignore
            main_image=main_image 
        )

    return ProductDetailsSchema(
            id=product.id,
            title=product.title,
            price=product.price, # type: ignore
            description=product.description,
            category_id=product.category_id,
            is_available=product.is_available,
            stock_quantity=product.stock_quantity,
            status=product.status,
            country_of_origin_id=product.country_of_origin_id,
            manufacturer_id=product.manufacturer_id,
            images=[ImageSchema.model_validate(img, from_attributes=True) for img in product.images],
            attributes=[AttributeSchema.model_validate(attr, from_attributes=True) for attr in product.attributes],
    )
