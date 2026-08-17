from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import relationship

from app.database import Base


class CrossoverSignal(Base):
    __tablename__ = "crossover_signals"

    id = Column(
        Integer,
        primary_key=True,
    )

    ticker_id = Column(
        Integer,
        ForeignKey("tickers.id"),
        nullable=False,
    )

    price_snapshot_id = Column(
        Integer,
        ForeignKey("price_snapshots.id"),
        nullable=False,
    )

    signal_type = Column(
        Enum(
            "golden_cross",
            "death_cross",
            name="signal_type",
        ),
        nullable=False,
    )

    short_ma = Column(
        Numeric(12, 4),
        nullable=False,
    )

    long_ma = Column(
        Numeric(12, 4),
        nullable=False,
    )

    detected_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    ticker = relationship(
        "Ticker",
        back_populates="crossover_signals",
    )

    price_snapshot = relationship(
        "PriceSnapshot",
        back_populates="signal",
    )
