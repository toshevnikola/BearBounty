from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Strategy])
def read_strategies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve strategies.
    """
    if crud.user.is_superuser(current_user):
        strategies = crud.strategy.get_multi(db, skip=skip, limit=limit)
    else:
        strategies = crud.strategy.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return strategies


@router.post("/", response_model=schemas.Strategy)
def create_strategy(
    *,
    db: Session = Depends(deps.get_db),
    strategy_in: schemas.StrategyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new strategy.
    """
    strategy = crud.strategy.create_with_owner(db=db, obj_in=strategy_in, owner_id=current_user.id)
    return strategy


@router.put("/{id}", response_model=schemas.Strategy)
def update_strategy(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    strategy_in: schemas.StrategyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an strategy.
    """
    strategy = crud.strategy.get(db=db, id=id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if not crud.user.is_superuser(current_user) and (strategy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    strategy = crud.strategy.update(db=db, db_obj=strategy, obj_in=strategy_in)
    return strategy


@router.get("/{id}", response_model=schemas.Strategy)
def read_strategy(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get strategy by ID.
    """
    strategy = crud.strategy.get(db=db, id=id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if not crud.user.is_superuser(current_user) and (strategy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return strategy


@router.delete("/{id}", response_model=schemas.Strategy)
def delete_strategy(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an strategy.
    """
    strategy = crud.strategy.get(db=db, id=id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if not crud.user.is_superuser(current_user) and (strategy.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    strategy = crud.strategy.remove(db=db, id=id)
    return strategy
