"""Images unique index

Revision ID: c0599329890a
Revises: e0961964f9b7
Create Date: 2025-05-02 14:55:16.713054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0599329890a'
down_revision: Union[str, None] = 'e0961964f9b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE UNIQUE INDEX uq_main_image_per_product
        ON images(product_id)
        WHERE is_main = TRUE;
    """)

def downgrade() -> None:
    op.execute("DROP INDEX uq_main_image_per_product")
