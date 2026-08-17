"""create price_snapshots table

Revision ID: 0003
Revises: 0002
Create Date: 2024-01-01 00:00:03

"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ticker_id", sa.Integer, sa.ForeignKey("tickers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("price", sa.Numeric(12, 4), nullable=False),
        sa.Column("volume", sa.BigInteger, nullable=False),
        sa.Column("captured_at", sa.DateTime, nullable=False),
        sa.Column("source", sa.String(100), nullable=False),
    )
    op.create_index("ix_price_snapshots_ticker_captured", "price_snapshots", ["ticker_id", "captured_at"])


def downgrade() -> None:
    op.drop_index("ix_price_snapshots_ticker_captured", table_name="price_snapshots")
    op.drop_table("price_snapshots")
