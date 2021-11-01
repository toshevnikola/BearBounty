from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app import crud
from app.schemas import Deal
from app.api import deps
from utils import get_current_user

router = APIRouter()


@router.get("/", response_model=List[Deal], status_code=status.HTTP_200_OK)
def get_deals(
    *,
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 500,
    db: Session = Depends(deps.get_db)
):
    current_user = get_current_user(Authorize)
    return crud.deal.get_by_user(db, current_user, skip=skip, limit=limit)


@router.get(
    "/user_exchange/{user_exchange_id}",
    response_model=List[Deal],
    status_code=status.HTTP_200_OK,
)
def get_deals_by_user_exchange(
    *,
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 500,
    db: Session = Depends(deps.get_db),
    user_exchange_id: int
):
    current_user = get_current_user(Authorize)
    user_exchange = crud.user_exchange.get(db=db, id=user_exchange_id)
    if not user_exchange:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Exchange not found"
        )
    if user_exchange.user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden User Exchange"
        )
    return crud.deal.get_by_user_exchange(
        db=db, user_exchange_id=user_exchange_id, skip=skip, limit=limit
    )
