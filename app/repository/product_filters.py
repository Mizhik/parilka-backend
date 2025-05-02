from typing import Optional, List
from uuid import UUID

from sqlalchemy import or_, and_
from sqlalchemy.sql import ClauseElement

from app.models.models import Product


def product_filters(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    manufacturer_ids: Optional[List[UUID]] = None,
) -> List[ClauseElement]:
    filters = []

    if min_price is not None:
        filters.append(
            or_(
                Product.discount_price >= min_price,
                and_(Product.discount_price.is_(None), Product.price >= min_price)
            )
        )

    if max_price is not None:
        filters.append(
            or_(
                Product.discount_price <= max_price,
                and_(Product.discount_price.is_(None), Product.price <= max_price)
            )
        )

    if manufacturer_ids:
        filters.append(Product.manufacturer_id.in_(manufacturer_ids))

    return filters


def apply_common_filters(stmt, filters, offset=None, limit=None):
    if filters:
        stmt = stmt.where(and_(*filters))
    if offset is not None:
        stmt = stmt.offset(offset)
    if limit is not None:
        stmt = stmt.limit(limit)
    return stmt
