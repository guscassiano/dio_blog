"""add user_id to posts with default

Revision ID: a7d392128249
Revises: e03c925a3753
Create Date: 2026-03-16 23:02:50.817644

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7d392128249"
down_revision: Union[str, Sequence[str], None] = "e03c925a3753"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Using 'batch_alter_table' context to get run in SQLite
    with op.batch_alter_table("posts") as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), server_default="1", nullable=True)
        )
        batch_op.alter_column(
            "published_at", existing_type=sa.TIMESTAMP(), nullable=False
        )
        batch_op.create_foreign_key(
            "fk_posts_users", "users", ["user_id"], ["id"], ondelete="CASCADE"
        )
        # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("posts") as batch_op:
        batch_op.drop_constraint("fk_posts_users", type_="foreignkey")
        batch_op.alter_column(
            "published_at", existing_type=sa.TIMESTAMP(), nullable=True
        )
        batch_op.drop_column("user_id")
    # ### end Alembic commands ###
