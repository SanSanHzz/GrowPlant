"""Create users table

Revision ID: 001
Revises:
Create Date: 2026-05-22
"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("github_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(39), nullable=False),
        sa.Column("display_name", sa.String(255), nullable=True),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.Column("encrypted_token", sa.LargeBinary(), nullable=False),
        sa.Column("token_nonce", sa.LargeBinary(), nullable=False),
        sa.Column(
            "github_connected_at", sa.DateTime(timezone=True), nullable=False
        ),
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
    op.create_index("idx_user_github_id", "users", ["github_id"], unique=True)
    op.create_index("idx_user_username", "users", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index("idx_user_username", table_name="users")
    op.drop_index("idx_user_github_id", table_name="users")
    op.drop_table("users")
