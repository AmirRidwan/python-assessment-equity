from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.portfolio_manager import PortfolioManager
from app.schemas import ManagerCreate, ManagerOut, ManagerUpdate

router = APIRouter()


@router.post(
    "",
    response_model=ManagerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_manager(
    manager_data: ManagerCreate,
    db: Session = Depends(get_db),
):
    existing_manager = (
        db.query(PortfolioManager)
        .filter(PortfolioManager.email == manager_data.email)
        .first()
    )

    if existing_manager:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    manager = PortfolioManager(
        name=manager_data.name,
        email=manager_data.email,
        seniority=manager_data.seniority,
        active=True,
    )

    db.add(manager)
    db.commit()
    db.refresh(manager)

    return manager


@router.get(
    "",
    response_model=list[ManagerOut],
)
def list_managers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * page_size

    managers = (
        db.query(PortfolioManager)
        .order_by(PortfolioManager.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return managers


@router.get(
    "/{manager_id}",
    response_model=ManagerOut,
)
def get_manager(
    manager_id: int,
    db: Session = Depends(get_db),
):
    manager = (
        db.query(PortfolioManager).filter(PortfolioManager.id == manager_id).first()
    )

    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio manager not found",
        )

    return manager


@router.put(
    "/{manager_id}",
    response_model=ManagerOut,
)
def update_manager(
    manager_id: int,
    manager_data: ManagerUpdate,
    db: Session = Depends(get_db),
):
    manager = (
        db.query(PortfolioManager).filter(PortfolioManager.id == manager_id).first()
    )

    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio manager not found",
        )

    if manager_data.email is not None:
        existing_manager = (
            db.query(PortfolioManager)
            .filter(
                PortfolioManager.email == manager_data.email,
                PortfolioManager.id != manager_id,
            )
            .first()
        )

        if existing_manager:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

    if manager_data.name is not None:
        manager.name = manager_data.name

    if manager_data.email is not None:
        manager.email = manager_data.email

    if manager_data.seniority is not None:
        manager.seniority = manager_data.seniority

    if manager_data.active is not None:
        manager.active = manager_data.active

    db.commit()
    db.refresh(manager)

    return manager


@router.delete(
    "/{manager_id}",
)
def delete_manager(manager_id: int):
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Manager deletion is not supported; deactivate the manager instead",
    )
