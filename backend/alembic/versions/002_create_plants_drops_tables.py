"""Create plants and drops tables

Revision ID: 002
Revises: 001
Create Date: 2026-05-22
"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "plants",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            unique=True,
            nullable=False,
        ),
        sa.Column("plant_type", sa.String(50), nullable=False),
        sa.Column("current_stage", sa.Integer(), server_default="1", nullable=False),
        sa.Column("total_drops", sa.Integer(), server_default="0", nullable=False),
        sa.Column("drops_in_stage", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("idx_plant_user", "plants", ["user_id"], unique=True)

    op.create_table(
        "drops",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "plant_id",
            UUID(as_uuid=True),
            sa.ForeignKey("plants.id"),
            nullable=False,
        ),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("source_repo", sa.String(255), nullable=False),
        sa.Column("github_event_id", sa.String(64), nullable=False),
        sa.Column("committed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("idx_drop_plant", "drops", ["plant_id"])
    op.create_index(
        "idx_drop_github_event", "drops", ["github_event_id"], unique=True
    )
    op.create_index(
        "idx_drop_created_at",
        "drops",
        ["plant_id", sa.text("created_at DESC")],
    )


def downgrade() -> None:
    op.drop_index("idx_drop_created_at", table_name="drops")
    op.drop_index("idx_drop_github_event", table_name="drops")
    op.drop_index("idx_drop_plant", table_name="drops")
    op.drop_table("drops")
    op.drop_index("idx_plant_user", table_name="plants")
    op.drop_table("plants")
