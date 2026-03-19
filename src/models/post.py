import sqlalchemy as sa

from src.database import metadata

posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String, nullable=False, unique=True),
    sa.Column("content", sa.String, nullable=False),
    sa.Column("published_at", sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column("published", sa.Boolean, default=False),
    sa.Column(
        "user_id",
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        server_default="1",
    ),
)
