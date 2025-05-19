"""Add default categories

Revision ID: dc2b40e15603
Revises: 1f777a01381b
Create Date: 2025-05-19 07:29:58.426863

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.functions import now


# revision identifiers, used by Alembic.
revision: str = "dc2b40e15603"
down_revision: Union[str, None] = "1f777a01381b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        f"INSERT INTO categories(id, create_at, update_at, title) VALUES('{uuid4()}', {now()}, {now()}, 'liquids')"
    )
    op.execute(
        f"INSERT INTO categories(id, create_at, update_at, title) VALUES('{uuid4()}', {now()}, {now()}, 'devices')"
    )
    op.execute(
        f"INSERT INTO categories(id, create_at, update_at, title) VALUES('{uuid4()}', {now()}, {now()}, 'components')"
    )
    op.execute(
        f"INSERT INTO categories(id, create_at, update_at, title) VALUES('{uuid4()}', {now()}, {now()}, 'hookah')"
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM categories WHERE title in ('liquids', 'devices', 'components', 'hookah')"
    )
