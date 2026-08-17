"""create portfolio_holdings table

Revision ID: 0004
Revises: 0003
Create Date: 2024-01-01 00:00:04

"""
from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "portfolio_holdings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("manager_id", sa.Integer, sa.ForeignKey("portfolio_managers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ticker_id", sa.Integer, sa.ForeignKey("tickers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_weight_pct", sa.Numeric(5, 2), nullable=False),
        sa.Column("added_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("manager_id", "ticker_id", name="uq_holdings_manager_ticker"),
    )


def downgrade() -> None:
    op.drop_table("portfolio_holdings")
