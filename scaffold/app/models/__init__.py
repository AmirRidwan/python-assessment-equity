# ─────────────────────────────────────────────────────────────────────────────
# Import every model module here so Base.metadata sees every table when
# Alembic autogenerates, and so `from app.models import PortfolioManager` works.
#
# TODO: Once you complete each model file below, also add the SQLAlchemy
# `relationship()` calls described here (the relationship() call itself goes
# INSIDE each model class in its own file — this list is just the checklist):
#
#   PortfolioManager.holdings   -> one PortfolioManager has many PortfolioHolding
#   PortfolioManager.reports    -> one PortfolioManager has many Report
#   Ticker.price_snapshots      -> one Ticker has many PriceSnapshot
#   Ticker.holdings             -> one Ticker has many PortfolioHolding
#   Ticker.crossover_signals    -> one Ticker has many CrossoverSignal
#   PriceSnapshot.ticker        -> many PriceSnapshot belong to one Ticker
#   PriceSnapshot.signal        -> one PriceSnapshot has one CrossoverSignal (uselist=False)
#   PortfolioHolding.manager    -> many PortfolioHolding belong to one PortfolioManager
#   PortfolioHolding.ticker     -> many PortfolioHolding belong to one Ticker
#   CrossoverSignal.ticker      -> many CrossoverSignal belong to one Ticker
#   CrossoverSignal.price_snapshot -> many CrossoverSignal belong to one PriceSnapshot
#   Report.manager              -> many Report belong to one PortfolioManager
# ─────────────────────────────────────────────────────────────────────────────

from app.models.portfolio_manager import PortfolioManager  # noqa: F401
from app.models.ticker import Ticker  # noqa: F401
from app.models.price_snapshot import PriceSnapshot  # noqa: F401
from app.models.portfolio_holding import PortfolioHolding  # noqa: F401
from app.models.crossover_signal import CrossoverSignal  # noqa: F401
from app.models.report import Report  # noqa: F401
