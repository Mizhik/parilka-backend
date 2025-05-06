from typing import Optional
from uuid import UUID

from pydantic import model_validator
from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    DECIMAL,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import  UUID as PGUUID
from sqlalchemy.sql.operators import as_
from app.models.enums import (Status,
                              Payment as PaymentEnum,
                              Delivery as DeliveryEnum,
                              ProductStatus as StatusEnum)
from app.models.base_model import Base

product_attribute_association = Table(
    "product_attribute",
    Base.metadata,
    Column(
        "product_id", PGUUID(as_uuid=True), ForeignKey("products.id"), primary_key=True
    ),
    Column(
        "attribute_id",
        PGUUID(as_uuid=True),
        ForeignKey("attributes.id"),
        primary_key=True,
    ),
)


class Product(Base):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=10, scale=2), nullable=False
    )
    discount_price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=10, scale=2), nullable=True
    )
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[StatusEnum] = mapped_column("status", Enum(StatusEnum), default=StatusEnum.NONE)

    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="product", cascade="all, delete-orphan", lazy="selectin"
    )

    category_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE", name="CategoryProductFK"),
        nullable=False,
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    subcategory_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("subcategories.id", ondelete="SET NULL", name="SubCategoryProductFK"),
        nullable=True,
    )
    subcategory: Mapped[Optional["SubCategory"]] = relationship("SubCategory", back_populates="products")

    country_of_origin_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("countries.id", ondelete="CASCADE", name="CountryOfOriginProductFK"),
        nullable=False,
    )
    country: Mapped["Country"] = relationship("Country", back_populates="products")

    manufacturer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("manufacturers.id", ondelete="CASCADE", name="ManufacturerProductFK"),
        nullable=False,
    )
    manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer", back_populates="products"
    )

    attributes: Mapped[list["Attribute"]] = relationship(
        secondary=product_attribute_association,
        back_populates="products",
    )

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.status == StatusEnum.DISCOUNT:
            if self.discount_price is None:
                raise ValueError("The discount_price field is required if the status is DISCOUNT.")
            if self.discount_price >= self.price:
                raise ValueError("discount_price must be less than price.")
        return self


class Image(Base):
    __tablename__ = "images"

    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean(), default=False)
    product_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    product: Mapped[Product] = relationship("Product", back_populates="images")


class Attribute(Base):
    __tablename__ = "attributes"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)

    products: Mapped[list["Product"]] = relationship(
        secondary=product_attribute_association,
        back_populates="attributes",
    )


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(50), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

class SubCategory(Base):
    __tablename__ = "subcategories"

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    display_title: Mapped[str] = mapped_column(String(150), nullable=False)

    parent_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL", name="SubCategoryParentFK"),
        nullable=False,
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="subcategory",
        lazy="selectin",
    )


class Country(Base):
    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="country",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="manufacturer",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class User(Base):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    product_review: Mapped[list["ProductReview"]] = relationship(
        "ProductReview",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    order: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"
    total_price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=10, scale=2), nullable=False
    )
    delivery_address: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[Status] = mapped_column("status", Enum(Status), default=Status.NEW)
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    payment_method_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False,
    )
    delivery_method_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("deliveries.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="order")
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    payment_method: Mapped["Payment"] = relationship(
        "Payment", back_populates="order", lazy="selectin"
    )
    delivery_method: Mapped["Delivery"] = relationship(
        "Delivery", back_populates="order", lazy="selectin"
    )


class OrderItem(Base):
    __tablename__ = "orderitems"
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    order: Mapped["Order"] = relationship(
        "Order", back_populates="order_items", lazy="selectin"
    )
    product_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    product: Mapped["Product"] = relationship("Product", lazy="selectin")


class ProductReview(Base):
    __tablename__ = "productreviews"
    review: Mapped[str] = mapped_column(String(1000), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="product_review")

    product_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    product: Mapped["Product"] = relationship("Product", lazy="selectin")


class Payment(Base):
    __tablename__ = "payments"
    name: Mapped[PaymentEnum] = mapped_column("name", Enum(PaymentEnum), default=None)
    order: Mapped["Order"] = relationship(
        "Order", back_populates="payment_method", lazy="selectin"
    )


class Delivery(Base):
    __tablename__ = "deliveries"
    name: Mapped[DeliveryEnum] = mapped_column("name", Enum(DeliveryEnum), default=None)
    order: Mapped["Order"] = relationship(
        "Order", back_populates="delivery_method", lazy="selectin"
    )
