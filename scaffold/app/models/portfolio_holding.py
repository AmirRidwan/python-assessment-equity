from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.database import Base


class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    id = Column(
        Integer,
        primary_key=True,
    )

    manager_id = Column(
        Integer,
        ForeignKey("portfolio_managers.id"),
        nullable=False,
    )

    ticker_id = Column(
        Integer,
        ForeignKey("tickers.id"),
        nullable=False,
    )

    target_weight_pct = Column(
        Numeric(5, 2),
        nullable=False,
    )

    added_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "manager_id",
            "ticker_id",
            name="uq_portfolio_holdings_manager_ticker",
        ),
    )

    manager = relationship(
        "PortfolioManager",
        back_populates="holdings",
    )

    ticker = relationship(
        "Ticker",
        back_populates="holdings",
    )
