from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
    )

    manager_id = Column(
        Integer,
        ForeignKey("portfolio_managers.id"),
        nullable=False,
    )

    date_from = Column(
        Date,
        nullable=False,
    )

    date_to = Column(
        Date,
        nullable=False,
    )

    filename = Column(
        String(200),
        nullable=False,
    )

    row_count = Column(
        Integer,
        nullable=False,
    )

    generated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    manager = relationship(
        "PortfolioManager",
        back_populates="reports",
    )
