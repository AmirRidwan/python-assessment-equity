from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# TODO: Implement the endpoints below.
# Refer to the Data Model / API Endpoint Reference / FR-1 in ASSESSMENT-BRIEF.md.
# ─────────────────────────────────────────────────────────────────────────────


# POST /managers
# Create a new portfolio manager.
# BUSINESS RULE: email must be unique — return 400 if it already exists.
@router.post("/")
def create_manager(db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}


# GET /managers
# List all managers, paginated.
@router.get("/")
def list_managers(db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}


# GET /managers/{manager_id}
# Get one manager or 404.
@router.get("/{manager_id}")
def get_manager(manager_id: int, db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}


# PUT /managers/{manager_id}
# Update a manager's fields.
@router.put("/{manager_id}")
def update_manager(manager_id: int, db: Session = Depends(get_db)):
    # TODO
    return {"message": "Not implemented"}


# DELETE /managers/{manager_id}
# Not supported — deactivate instead so historical references stay valid.
@router.delete("/{manager_id}", status_code=405)
def delete_manager(manager_id: int):
    return {"detail": "Managers cannot be deleted — set active=false via PUT instead."}
