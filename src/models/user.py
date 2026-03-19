import sqlalchemy as sa

from src.database import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("nickname", sa.String, nullable=False, unique=True),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column("active", sa.Boolean, default=True),
    sa.Column("role", sa.String, nullable=False, server_default="user"),
)
