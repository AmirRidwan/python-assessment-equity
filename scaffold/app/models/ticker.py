from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True)

    symbol = Column(
        String(10),
        nullable=False,
        unique=True,
    )

    company_name = Column(
        String(150),
        nullable=False,
    )

    sector = Column(
        String(50),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    price_snapshots = relationship(
        "PriceSnapshot",
        back_populates="ticker",
    )

    holdings = relationship(
        "PortfolioHolding",
        back_populates="ticker",
    )

    crossover_signals = relationship(
        "CrossoverSignal",
        back_populates="ticker",
    )
