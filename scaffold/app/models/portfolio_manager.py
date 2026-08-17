from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class PortfolioManager(Base):
    __tablename__ = "portfolio_managers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    seniority = Column(
        Enum(
            "analyst",
            "associate",
            "principal",
            name="seniority_enum",
        ),
        nullable=False,
    )

    active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    holdings = relationship(
        "PortfolioHolding",
        back_populates="manager",
    )

    reports = relationship(
        "Report",
        back_populates="manager",
    )
