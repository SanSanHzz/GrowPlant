"""Increase github_event_id length to 255

Revision ID: 003
Revises: 002
Create Date: 2026-05-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "drops",
        "github_event_id",
        type_=sa.String(255),
        existing_type=sa.String(64),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "drops",
        "github_event_id",
        type_=sa.String(64),
        existing_type=sa.String(255),
        nullable=False,
    )
