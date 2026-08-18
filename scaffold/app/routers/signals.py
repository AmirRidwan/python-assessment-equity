from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.crossover_signal import CrossoverSignal
from app.models.ticker import Ticker
from app.schemas import CrossoverSignalOut

router = APIRouter()


@router.get(
    "/",
    response_model=list[CrossoverSignalOut],
)
def list_signals(
    ticker_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if ticker_id is not None:
        ticker = db.query(Ticker).filter(Ticker.id == ticker_id).first()

        if ticker is None:
            raise HTTPException(
                status_code=404,
                detail="Ticker not found",
            )

    query = db.query(CrossoverSignal)

    if ticker_id is not None:
        query = query.filter(CrossoverSignal.ticker_id == ticker_id)

    offset = (page - 1) * page_size

    return (
        query.order_by(CrossoverSignal.detected_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
