from app.database import Base

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Define the `portfolio_holdings` table (junction table — the domain-
# unique scoping concept for this assessment: each manager's portfolio is
# isolated, AND the sum of target_weight_pct across a manager's entire
# portfolio must never exceed 100).
#
# Columns:
#   id                  — Integer, primary key
#   manager_id          — Integer, ForeignKey("portfolio_managers.id"), not null
#   ticker_id           — Integer, ForeignKey("tickers.id"), not null
#   target_weight_pct   — Numeric(5, 2), not null
#   added_at            — DateTime, not null, server default now()
#   UniqueConstraint(manager_id, ticker_id)
#
# Also add:
#   manager = relationship("PortfolioManager", back_populates="holdings")
#   ticker = relationship("Ticker", back_populates="holdings")
#
# BUSINESS RULE (enforced in the router, not here): before inserting or
# updating a holding, sum target_weight_pct across ALL of this manager's
# holdings (excluding the row being updated, if any) plus the new value —
# reject with 400 if the total would exceed 100.
# ─────────────────────────────────────────────────────────────────────────────


class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    # TODO: columns and relationships go here
    pass
