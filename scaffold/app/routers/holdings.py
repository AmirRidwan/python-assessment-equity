from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.business_logic.portfolio import (
    validate_total_weight,
    validate_updated_weight,
)
from app.database import get_db
from app.dependencies import get_current_manager
from app.models.portfolio_holding import PortfolioHolding
from app.models.ticker import Ticker
from app.schemas import HoldingCreate, HoldingOut, HoldingUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=HoldingOut,
    status_code=status.HTTP_201_CREATED,
)
def add_holding(
    holding_data: HoldingCreate,
    db: Session = Depends(get_db),
    acting_manager=Depends(get_current_manager),
):
    if not acting_manager.active:
        raise HTTPException(
            status_code=400,
            detail="Portfolio manager is inactive",
        )

    ticker = db.query(Ticker).filter(Ticker.id == holding_data.ticker_id).first()

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

    existing_holding = (
        db.query(PortfolioHolding)
        .filter(
            PortfolioHolding.manager_id == acting_manager.id,
            PortfolioHolding.ticker_id == holding_data.ticker_id,
        )
        .first()
    )

    if existing_holding is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticker is already in your portfolio",
        )

    existing_weights = [
        holding.target_weight_pct
        for holding in (
            db.query(PortfolioHolding)
            .filter(PortfolioHolding.manager_id == acting_manager.id)
            .all()
        )
    ]

    new_weight = Decimal(str(holding_data.target_weight_pct))

    if not validate_total_weight(
        existing_weights,
        new_weight,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Total target weight would exceed 100%",
        )

    holding = PortfolioHolding(
        manager_id=acting_manager.id,
        ticker_id=holding_data.ticker_id,
        target_weight_pct=new_weight,
    )

    db.add(holding)
    db.commit()
    db.refresh(holding)

    return holding


@router.get(
    "/",
    response_model=list[HoldingOut],
)
def get_holdings(
    db: Session = Depends(get_db),
    acting_manager=Depends(get_current_manager),
):
    if not acting_manager.active:
        raise HTTPException(
            status_code=400,
            detail="Portfolio manager is inactive",
        )

    return (
        db.query(PortfolioHolding)
        .filter(PortfolioHolding.manager_id == acting_manager.id)
        .order_by(PortfolioHolding.id)
        .all()
    )


@router.put(
    "/{ticker_id}",
    response_model=HoldingOut,
)
def update_holding(
    ticker_id: int,
    holding_data: HoldingUpdate,
    db: Session = Depends(get_db),
    acting_manager=Depends(get_current_manager),
):
    if not acting_manager.active:
        raise HTTPException(
            status_code=400,
            detail="Portfolio manager is inactive",
        )

    holding = (
        db.query(PortfolioHolding)
        .filter(
            PortfolioHolding.manager_id == acting_manager.id,
            PortfolioHolding.ticker_id == ticker_id,
        )
        .first()
    )

    if holding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found in your portfolio",
        )

    existing_weights = [
        current_holding.target_weight_pct
        for current_holding in (
            db.query(PortfolioHolding)
            .filter(PortfolioHolding.manager_id == acting_manager.id)
            .all()
        )
    ]

    new_weight = Decimal(str(holding_data.target_weight_pct))

    if not validate_updated_weight(
        existing_weights,
        holding.target_weight_pct,
        new_weight,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Total target weight would exceed 100%",
        )

    holding.target_weight_pct = new_weight

    db.commit()
    db.refresh(holding)

    return holding


@router.delete(
    "/{ticker_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_holding(
    ticker_id: int,
    db: Session = Depends(get_db),
    acting_manager=Depends(get_current_manager),
):
    if not acting_manager.active:
        raise HTTPException(
            status_code=400,
            detail="Portfolio manager is inactive",
        )

    holding = (
        db.query(PortfolioHolding)
        .filter(
            PortfolioHolding.manager_id == acting_manager.id,
            PortfolioHolding.ticker_id == ticker_id,
        )
        .first()
    )

    if holding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found in your portfolio",
        )

    db.delete(holding)
    db.commit()

    return None
