"""create crossover_signals table

Revision ID: 0005
Revises: 0004
Create Date: 2024-01-01 00:00:05

"""
from alembic import op
import sqlalchemy as sa

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None

signal_type_enum = sa.Enum("golden_cross", "death_cross", name="signal_type_enum")


def upgrade() -> None:
    signal_type_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "crossover_signals",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ticker_id", sa.Integer, sa.ForeignKey("tickers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("price_snapshot_id", sa.Integer, sa.ForeignKey("price_snapshots.id", ondelete="CASCADE"), nullable=False),
        sa.Column("signal_type", signal_type_enum, nullable=False),
        sa.Column("short_ma", sa.Numeric(12, 4), nullable=False),
        sa.Column("long_ma", sa.Numeric(12, 4), nullable=False),
        sa.Column("detected_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("crossover_signals")
    signal_type_enum.drop(op.get_bind(), checkfirst=True)
