from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_manager

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Implement the endpoints below.
# Refer to the API Endpoint Reference / FR-3 in ASSESSMENT-BRIEF.md.
#
# This is the domain-unique scoping concept for this assessment — every
# endpoint here operates ONLY on the requesting manager's own rows. GET
# /holdings must never leak another manager's holdings (the isolation test),
# and POST/PUT must enforce that the SUM of target_weight_pct across the
# manager's entire portfolio never exceeds 100 (the aggregate-constraint
# test — unique to this domain, not present in treasury/commodity).
# ─────────────────────────────────────────────────────────────────────────────


# POST /holdings
# Add a ticker to the requesting manager's portfolio with a target_weight_pct.
# BUSINESS RULE: cannot add the same ticker twice — return 400.
# BUSINESS RULE: sum of target_weight_pct across the manager's ENTIRE
#   portfolio (existing + new) must not exceed 100 — return 400 otherwise.
@router.post("/")
def add_holding(db: Session = Depends(get_db), acting_manager=Depends(get_current_manager)):
    # TODO
    return {"message": "Not implemented"}


# GET /holdings
# Return ONLY the requesting manager's own portfolio.
@router.get("/")
def get_holdings(db: Session = Depends(get_db), acting_manager=Depends(get_current_manager)):
    # TODO
    return {"message": "Not implemented"}


# PUT /holdings/{ticker_id}
# Update the target_weight_pct for a ticker already in the manager's portfolio.
# BUSINESS RULE: same 100%-total constraint applies — recompute the total
#   excluding the OLD value for this ticker before checking the new one.
@router.put("/{ticker_id}")
def update_holding(ticker_id: int, db: Session = Depends(get_db), acting_manager=Depends(get_current_manager)):
    # TODO
    return {"message": "Not implemented"}


# DELETE /holdings/{ticker_id}
# Remove a ticker from the requesting manager's portfolio.
# Removing something not held returns 404.
@router.delete("/{ticker_id}")
def remove_holding(ticker_id: int, db: Session = Depends(get_db), acting_manager=Depends(get_current_manager)):
    # TODO
    return {"message": "Not implemented"}
