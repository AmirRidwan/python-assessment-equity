from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Complete each Pydantic schema below.
#
# Naming convention:
#   <Entity>Create — fields accepted on POST
#   <Entity>Update — fields accepted on PUT (all optional)
#   <Entity>Out     — fields returned in responses (config: from_attributes=True)
# ─────────────────────────────────────────────────────────────────────────────


# ── Portfolio Manager ────────────────────────────────────────────────────────
class ManagerCreate(BaseModel):
    # TODO: name: str, email: EmailStr, seniority: str (one of "analyst","associate","principal")
    pass


class ManagerUpdate(BaseModel):
    # TODO: all fields optional — name, email, seniority, active
    pass


class ManagerOut(BaseModel):
    # TODO: id, name, email, seniority, active, created_at
    class Config:
        from_attributes = True


# ── Ticker ───────────────────────────────────────────────────────────────────
class TickerOut(BaseModel):
    # TODO: id, symbol, company_name, sector, is_active
    class Config:
        from_attributes = True


# ── Price Snapshot ───────────────────────────────────────────────────────────
class PriceSnapshotCreate(BaseModel):
    # TODO: price: float (> 0), volume: int (>= 0), captured_at: datetime, source: str
    pass


class PriceSnapshotOut(BaseModel):
    # TODO: id, ticker_id, price, volume, captured_at, source
    class Config:
        from_attributes = True


# ── Portfolio Holding ────────────────────────────────────────────────────────
class HoldingCreate(BaseModel):
    # TODO: ticker_id: int, target_weight_pct: float
    pass


class HoldingUpdate(BaseModel):
    # TODO: target_weight_pct: float
    pass


class HoldingOut(BaseModel):
    # TODO: id, manager_id, ticker_id, target_weight_pct, added_at
    class Config:
        from_attributes = True


# ── Crossover Signal ─────────────────────────────────────────────────────────
class CrossoverSignalOut(BaseModel):
    # TODO: id, ticker_id, price_snapshot_id, signal_type, short_ma, long_ma, detected_at
    class Config:
        from_attributes = True


# ── Report ───────────────────────────────────────────────────────────────────
class ReportCreate(BaseModel):
    # TODO: date_from: date, date_to: date
    # Note: like the commodity domain (and unlike treasury), this does NOT
    # take an explicit ticker list — the report always covers the requesting
    # manager's current portfolio (see FR-4.3 in ASSESSMENT-BRIEF.md).
    pass


class ReportOut(BaseModel):
    # TODO: id, manager_id, date_from, date_to, filename, row_count, generated_at
    class Config:
        from_attributes = True
