from app.database import Base

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Define the `tickers` table (seeded, read-only reference table).
#
# Columns:
#   id             — Integer, primary key
#   symbol         — String(10), not null, unique
#   company_name   — String(150), not null
#   sector         — String(50), not null
#   is_active      — Boolean, not null, default True
#
# Also add:
#   price_snapshots = relationship("PriceSnapshot", back_populates="ticker")
#   holdings = relationship("PortfolioHolding", back_populates="ticker")
#   crossover_signals = relationship("CrossoverSignal", back_populates="ticker")
# ─────────────────────────────────────────────────────────────────────────────


class Ticker(Base):
    __tablename__ = "tickers"

    # TODO: columns and relationships go here
    pass
