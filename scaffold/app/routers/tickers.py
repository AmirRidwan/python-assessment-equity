from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.business_logic.crossover import detect_crossover
from app.business_logic.moving_average import calculate_moving_average
from app.database import get_db
from app.models.crossover_signal import CrossoverSignal
from app.models.price_snapshot import PriceSnapshot
from app.models.ticker import Ticker
from app.schemas import PriceSnapshotCreate, PriceSnapshotOut, TickerOut

router = APIRouter()


@router.get(
    "/",
    response_model=list[TickerOut],
)
def list_tickers(
    db: Session = Depends(get_db),
):
    return db.query(Ticker).filter(Ticker.is_active.is_(True)).order_by(Ticker.id).all()


@router.post(
    "/{ticker_id}/prices",
    response_model=PriceSnapshotOut,
    status_code=status.HTTP_201_CREATED,
)
def record_price(
    ticker_id: int,
    price_data: PriceSnapshotCreate,
    db: Session = Depends(get_db),
):
    ticker = db.query(Ticker).filter(Ticker.id == ticker_id).first()

    if ticker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticker not found",
        )

    if not ticker.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticker is inactive",
        )

    latest_snapshot = (
        db.query(PriceSnapshot)
        .filter(PriceSnapshot.ticker_id == ticker_id)
        .order_by(PriceSnapshot.captured_at.desc())
        .first()
    )

    if latest_snapshot is not None:
        if price_data.captured_at <= latest_snapshot.captured_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "captured_at must be later than the "
                    "ticker's most recent snapshot"
                ),
            )

    snapshot = PriceSnapshot(
        ticker_id=ticker_id,
        price=price_data.price,
        volume=price_data.volume,
        captured_at=price_data.captured_at,
        source=price_data.source,
    )

    db.add(snapshot)
    db.flush()

    snapshots = (
        db.query(PriceSnapshot)
        .filter(PriceSnapshot.ticker_id == ticker_id)
        .order_by(PriceSnapshot.captured_at.asc())
        .all()
    )

    if len(snapshots) >= 20:
        prices = [snapshot.price for snapshot in snapshots]

        short_mas = calculate_moving_average(prices, 5)
        long_mas = calculate_moving_average(prices, 20)

        current_index = len(snapshots) - 1

        current_short_ma = short_mas[current_index]
        current_long_ma = long_mas[current_index]

        # A previous 20-day MA requires at least 21 snapshots.
        # Until then, the current moving averages can be calculated,
        # but a crossover cannot be compared against a previous
        # complete 20-day state.
        if current_index >= 20:
            previous_short_ma = short_mas[current_index - 1]
            previous_long_ma = long_mas[current_index - 1]

            signal_type = detect_crossover(
                previous_short_ma,
                previous_long_ma,
                current_short_ma,
                current_long_ma,
            )

            if signal_type is not None:
                existing_signal = (
                    db.query(CrossoverSignal)
                    .filter(CrossoverSignal.price_snapshot_id == snapshot.id)
                    .first()
                )

                if existing_signal is None:
                    signal = CrossoverSignal(
                        ticker_id=ticker_id,
                        price_snapshot_id=snapshot.id,
                        signal_type=signal_type,
                        short_ma=current_short_ma,
                        long_ma=current_long_ma,
                    )

                    db.add(signal)

    db.commit()
    db.refresh(snapshot)

    return snapshot


@router.get(
    "/{ticker_id}/prices",
    response_model=list[PriceSnapshotOut],
)
def list_prices(
    ticker_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    ticker = db.query(Ticker).filter(Ticker.id == ticker_id).first()

    if ticker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticker not found",
        )

    offset = (page - 1) * page_size

    return (
        db.query(PriceSnapshot)
        .filter(PriceSnapshot.ticker_id == ticker_id)
        .order_by(PriceSnapshot.captured_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
