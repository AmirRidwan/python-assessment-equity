"""create portfolio_managers table

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:01

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

seniority_enum = sa.Enum("analyst", "associate", "principal", name="seniority_enum")


def upgrade() -> None:
    seniority_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "portfolio_managers",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(150), nullable=False, unique=True),
        sa.Column("seniority", seniority_enum, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("portfolio_managers")
    seniority_enum.drop(op.get_bind(), checkfirst=True)
