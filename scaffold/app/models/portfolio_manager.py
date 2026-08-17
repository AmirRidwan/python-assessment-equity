from app.database import Base

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Define the `portfolio_managers` table.
#
# Columns:
#   id          — Integer, primary key
#   name        — String(100), not null
#   email       — String(150), not null, unique
#   seniority   — Enum("analyst", "associate", "principal"), not null
#   active      — Boolean, not null, default True
#   created_at  — DateTime, not null, server default now()
#
# Also add:
#   holdings = relationship("PortfolioHolding", back_populates="manager")
#   reports = relationship("Report", back_populates="manager")
# ─────────────────────────────────────────────────────────────────────────────


class PortfolioManager(Base):
    __tablename__ = "portfolio_managers"

    # TODO: columns and relationships go here
    pass
