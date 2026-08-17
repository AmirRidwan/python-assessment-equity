from app.database import Base

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Define the `price_snapshots` table.
#
# Columns:
#   id           — Integer, primary key
#   ticker_id    — Integer, ForeignKey("tickers.id"), not null
#   price        — Numeric(12, 4), not null (must be > 0)
#   volume       — BigInteger, not null (must be >= 0)
#   captured_at  — DateTime, not null
#   source       — String(100), not null
#
# Also add:
#   ticker = relationship("Ticker", back_populates="price_snapshots")
#   signal = relationship("CrossoverSignal", back_populates="price_snapshot", uselist=False)
#
# BUSINESS RULE (enforced in the router, not here): a new snapshot's
# captured_at must be later than the ticker's most recent existing snapshot.
# ─────────────────────────────────────────────────────────────────────────────


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    # TODO: columns and relationships go here
    pass
