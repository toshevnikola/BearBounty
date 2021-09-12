from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import schemas
from api import deps
from utils import get_current_user
from app import crud

router = APIRouter()


@router.post("/", response_model=schemas.DCABot, status_code=status.HTTP_201_CREATED)
def create_bot(
    *,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(deps.get_db),
    bot_in: schemas.DCABotCreate,
):
    current_user = get_current_user(Authorize)
    user_exchange = crud.user_exchange.get(db=db, id=bot_in.user_exchange_id)
    if not user_exchange:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Exchange not found"
        )
    if user_exchange.user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden User Exchange"
        )
    return crud.dca_bot.create(db=db, obj_in=bot_in)


@router.get(
    "/{user_exchange_id}",
    response_model=List[schemas.DCABot],
    status_code=status.HTTP_200_OK,
)
def get_user_exchange_bots(
    *,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(deps.get_db),
    user_exchange_id: int,
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

    return crud.dca_bot.get_by_user_exchange(db=db, user_exchange_id=user_exchange_id)


@router.get("/", response_model=List[schemas.DCABot], status_code=status.HTTP_200_OK)
def get_user_bots(
    *, Authorize: AuthJWT = Depends(), db: Session = Depends(deps.get_db),
):
    current_user = get_current_user(Authorize)
    return crud.dca_bot.get_by_user(db=db, user_id=current_user)


@router.delete("/{id}", response_model=schemas.DCABot, status_code=status.HTTP_200_OK)
def delete_bot(
    *, Authorize: AuthJWT = Depends(), db: Session = Depends(deps.get_db), id: int
):
    current_user = get_current_user(Authorize)
    bot = crud.dca_bot.get_single(db=db, id=id, user_id=current_user)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return crud.dca_bot.remove(db=db, id=id)
