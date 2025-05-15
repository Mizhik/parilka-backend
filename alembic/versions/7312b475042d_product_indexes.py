"""Product indexes

Revision ID: 7312b475042d
Revises: 1ecb4422f8e9
Create Date: 2025-05-15 12:00:30.430274

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7312b475042d"
down_revision: Union[str, None] = "1ecb4422f8e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX idx_products_subcat_available_created
        ON products (subcategory_id, is_available, create_at DESC);
    """)
    op.execute("""
        CREATE INDEX idx_products_manufacturer_id
        ON products (manufacturer_id);
    """)
    op.execute("""
        CREATE INDEX idx_products_available_only
        ON products (subcategory_id, create_at DESC)
        WHERE is_available = TRUE;
    """)


def downgrade() -> None:
    op.execute("""
        DROP INDEX idx_products_subcat_available_created;
        DROP INDEX idx_products_manufacturer_id;
        DROP INDEX idx_products_available_only;
    """)
