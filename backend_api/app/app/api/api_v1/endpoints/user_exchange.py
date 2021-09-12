from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import Response
from fastapi_jwt_auth import AuthJWT
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core.config import settings
from app.api import deps
from utils import get_current_user

router = APIRouter()


@router.post(
    "/", response_model=schemas.UserExchange, status_code=status.HTTP_201_CREATED
)
def create_user_exchange(
    *,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(deps.get_db),
    user_exchange_in: schemas.UserExchangeCreate,
) -> Any:
    """
    Create new user_exchange.
    """
    current_user = get_current_user(Authorize)
    user_exchange = crud.user_exchange.get_by_user_and_exchange(
        db, user_id=current_user, exchange_id=user_exchange_in.exchange_id
    )
    if user_exchange:
        raise HTTPException(
            status_code=400, detail="Already connected to this exchange",
        )
    else:
        "CONNECT TO PROVIDED EXCHANGE"

        user_exchange = crud.user_exchange.create_with_user(
            db, obj_in=user_exchange_in, user_id=current_user
        )

    return user_exchange


@router.get(
    "/", response_model=List[schemas.UserExchange], status_code=status.HTTP_200_OK
)
def get_user_exchanges(
    *, Authorize: AuthJWT = Depends(), db: Session = Depends(deps.get_db)
):
    current_user = get_current_user(Authorize)
    return crud.user_exchange.get_by_user(db, user_id=current_user)


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserExchange
)
async def delete_user_exchange(
    *, Authorize: AuthJWT = Depends(), db: Session = Depends(deps.get_db), id: int
) -> None:
    current_user = get_current_user(Authorize)
    user_exchange = crud.user_exchange.get(db=db, id=id)
    if not user_exchange:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if user_exchange.user_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return crud.user_exchange.remove(db=db, id=id)
