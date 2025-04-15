"""Add constructors to contstructor table

Revision ID: 11c021235874
Revises: 8cf65a138c0c
Create Date: 2025-04-08 15:08:46.011808

"""
from typing import Sequence, Union
from uuid import UUID
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.functions import now
from sqlalchemy.types import Uuid

from app.models.enums import ConstructorTag


# revision identifiers, used by Alembic.
revision: str = '11c021235874'
down_revision: Union[str, None] = '8cf65a138c0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    constructor = sa.table("constructor", 
    sa.Column('tag', sa.Enum(ConstructorTag, name='constructortag')),
    sa.Column('component_data', postgresql.JSONB(astext_type=sa.Text())),
    sa.Column('id', sa.UUID()),
    sa.Column('create_at', sa.DateTime()),
    sa.Column('update_at', sa.DateTime()),
)
    op.execute(
        constructor.insert()
        .values([
            {
                "id": str(uuid.uuid4()),
                "tag": ConstructorTag.TOP_BANNER,
                "component_data": [],
                "create_at": now(),
                "update_at": now()
            },
            {
                "id": str(uuid.uuid4()),
                "tag": ConstructorTag.ACCORDION, "component_data": [],
                "create_at": now(),
                "update_at": now()
            }
        ])
    )


def downgrade() -> None:
    constructor = sa.table("constructor", 
    sa.Column('tag', sa.Enum('TOP_BANNER', 'ACCORDION', name='constructortag'), nullable=False))
    op.execute(
        constructor.delete()
        .where(constructor.c.tag.in_([tag.value for tag in ConstructorTag]))
    )
