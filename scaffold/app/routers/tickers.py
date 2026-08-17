from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Implement the endpoints below.
# Refer to the Data Model / API Endpoint Reference / FR-2, FR-4.1 in ASSESSMENT-BRIEF.md.
# ─────────────────────────────────────────────────────────────────────────────


# GET /tickers
# List the seeded reference table of tracked tickers (read-only).
@router.get("/")
def list_tickers(db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}


# POST /tickers/{ticker_id}/prices
# Record a new daily price snapshot for a ticker.
# BUSINESS RULE: price must be > 0; volume must be >= 0.
# BUSINESS RULE: captured_at must be later than the ticker's most recent
#   existing snapshot — return 400 otherwise.
# BUSINESS RULE (FR-4.1): once the ticker has at least 20 price snapshots
#   (including this new one), compute the 5-day and 20-day moving averages.
#   If the short MA crosses from below to above the long MA (comparing this
#   snapshot's state to the immediately preceding snapshot's state), create a
#   CrossoverSignal with signal_type="golden_cross"; if it crosses the other
#   way, signal_type="death_cross". Fewer than 20 snapshots -> no signal, not
#   an error.
@router.post("/{ticker_id}/prices")
def record_price(ticker_id: int, db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}


# GET /tickers/{ticker_id}/prices
# List price history for a ticker, paginated, most recent first.
@router.get("/{ticker_id}/prices")
def list_prices(ticker_id: int, db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}
