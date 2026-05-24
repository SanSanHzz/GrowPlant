"""Add name column to plants table

Revision ID: 005
Revises: 004
Create Date: 2026-05-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "plants",
        sa.Column("name", sa.String(100), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("plants", "name")
