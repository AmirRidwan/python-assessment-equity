from datetime import date, datetime
from typing import Literal
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ── Portfolio Manager ────────────────────────────────────────────────────────
ManagerSeniority = Literal["analyst", "associate", "principal"]


class ManagerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    seniority: ManagerSeniority


class ManagerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    seniority: ManagerSeniority | None = None
    active: bool | None = None


class ManagerOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    seniority: ManagerSeniority
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Ticker ───────────────────────────────────────────────────────────────────
class TickerOut(BaseModel):
    id: int
    symbol: str
    company_name: str
    sector: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ── Price Snapshot ───────────────────────────────────────────────────────────
class PriceSnapshotCreate(BaseModel):
    price: Decimal = Field(..., gt=0)
    volume: int = Field(..., ge=0)
    captured_at: datetime
    source: str = Field(..., min_length=1, max_length=100)


class PriceSnapshotOut(BaseModel):
    id: int
    ticker_id: int
    price: Decimal
    volume: int
    captured_at: datetime
    source: str

    model_config = ConfigDict(from_attributes=True)


# ── Portfolio Holding ────────────────────────────────────────────────────────
class HoldingCreate(BaseModel):
    ticker_id: int
    target_weight_pct: Decimal = Field(..., gt=0, le=100)


class HoldingUpdate(BaseModel):
    target_weight_pct: Decimal = Field(..., gt=0, le=100)


class HoldingOut(BaseModel):
    id: int
    manager_id: int
    ticker_id: int
    target_weight_pct: Decimal
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Crossover Signal ─────────────────────────────────────────────────────────
SignalType = Literal["golden_cross", "death_cross"]


class CrossoverSignalOut(BaseModel):
    id: int
    ticker_id: int
    price_snapshot_id: int
    signal_type: SignalType
    short_ma: Decimal
    long_ma: Decimal
    detected_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Report ───────────────────────────────────────────────────────────────────
class ReportCreate(BaseModel):
    date_from: date
    date_to: date


class ReportOut(BaseModel):
    id: int
    manager_id: int
    date_from: date
    date_to: date
    filename: str
    row_count: int
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
