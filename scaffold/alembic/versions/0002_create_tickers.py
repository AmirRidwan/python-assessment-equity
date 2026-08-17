"""create tickers table

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-01 00:00:02

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tickers",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.String(10), nullable=False, unique=True),
        sa.Column("company_name", sa.String(150), nullable=False),
        sa.Column("sector", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_table("tickers")
