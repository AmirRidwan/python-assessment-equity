from app.database import Base

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Define the `crossover_signals` table.
#
# Columns:
#   id                  — Integer, primary key
#   ticker_id           — Integer, ForeignKey("tickers.id"), not null
#   price_snapshot_id   — Integer, ForeignKey("price_snapshots.id"), not null
#   signal_type         — Enum("golden_cross", "death_cross"), not null
#   short_ma            — Numeric(12, 4), not null — the 5-day average at detection time
#   long_ma             — Numeric(12, 4), not null — the 20-day average at detection time
#   detected_at         — DateTime, not null, server default now()
#
# Also add:
#   ticker = relationship("Ticker", back_populates="crossover_signals")
#   price_snapshot = relationship("PriceSnapshot", back_populates="signal")
#
# BUSINESS RULE (enforced in the router, not here): only compute a signal once
# a ticker has at least 20 price snapshots. signal_type is always derived from
# the actual short_ma/long_ma comparison — never settable directly by a client.
# ─────────────────────────────────────────────────────────────────────────────


class CrossoverSignal(Base):
    __tablename__ = "crossover_signals"

    # TODO: columns and relationships go here
    pass
