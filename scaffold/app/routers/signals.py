from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Implement the endpoint below.
# Refer to the API Endpoint Reference / FR-4.2 in ASSESSMENT-BRIEF.md.
# ─────────────────────────────────────────────────────────────────────────────


# GET /signals
# List crossover signals, filterable by ?ticker_id=, paginated.
@router.get("/")
def list_signals(ticker_id: Optional[int] = None, db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}
