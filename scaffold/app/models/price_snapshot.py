from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id = Column(
        Integer,
        primary_key=True,
    )

    ticker_id = Column(
        Integer,
        ForeignKey("tickers.id"),
        nullable=False,
    )

    price = Column(
        Numeric(12, 4),
        nullable=False,
    )

    volume = Column(
        BigInteger,
        nullable=False,
    )

    captured_at = Column(
        DateTime,
        nullable=False,
    )

    source = Column(
        String(100),
        nullable=False,
    )

    ticker = relationship(
        "Ticker",
        back_populates="price_snapshots",
    )

    signal = relationship(
        "CrossoverSignal",
        back_populates="price_snapshot",
        uselist=False,
    )
