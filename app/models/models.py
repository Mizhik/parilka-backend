from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, DECIMAL, TIMESTAMP, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base_model import Base


product_attribute_association = Table(
    "product_attribute",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("attribute_id", Integer, ForeignKey("attributes.id"), primary_key=True),
)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=10, scale=2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    images: Mapped[list["Image"]] = relationship(
        "Image",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    category_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    country_of_origin_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("countries.id", ondelete="CASCADE"),
        nullable=True
    )
    country: Mapped["Country"] = relationship("Country", back_populates="products")

    manufacturer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("manufacturers.id", ondelete="CASCADE"),
        nullable=True
    )
    manufacturer: Mapped["Manufacturer"] = relationship("Manufacturer", back_populates="products")

    attributes: Mapped[list["Attribute"]] = relationship(
        secondary=product_attribute_association,
        back_populates="products",
    )


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    product_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False
    )

    product: Mapped[Product] = relationship(
        "Product", back_populates="images"
    )


class Attribute(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=True)

    products: Mapped[list["Product"]] = relationship(
        secondary=product_attribute_association,
        back_populates="attributes",
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    product: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="country",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    product: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="manufactures",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
