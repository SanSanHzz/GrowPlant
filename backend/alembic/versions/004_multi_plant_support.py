"""Multi-plant support: remove user_id unique, add is_active

Revision ID: 004
Revises: 003
Create Date: 2026-05-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("plants_user_id_key", "plants", type_="unique")
    op.create_index("idx_plant_user", "plants", ["user_id"])
    op.add_column(
        "plants",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("plants", "is_active")
    op.drop_index("idx_plant_user", table_name="plants")
    op.create_unique_constraint("plants_user_id_key", "plants", ["user_id"])
