from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.portfolio_manager import PortfolioManager


def get_current_manager(
    x_manager_id: int = Header(..., description="Login-As simulation — the acting manager's id"),
    db: Session = Depends(get_db),
) -> PortfolioManager:
    """Fully wired — do not modify.

    Resolves the X-Manager-Id header to a PortfolioManager row. Whether that
    manager is allowed to perform the specific action being requested is a
    BUSINESS RULE and is checked inside the route handler, not here.
    """
    manager = db.get(PortfolioManager, x_manager_id)
    if manager is None:
        raise HTTPException(status_code=401, detail="Unknown X-Manager-Id")
    return manager
