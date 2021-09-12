from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core.config import settings
from app.api import deps

router = APIRouter()

#
# @router.post("/", response_model=schemas.Exchange, status_code=status.HTTP_201_CREATED)
# def create_exchange(
#         *,
#         db: Session = Depends(deps.get_db),
#         exchange_in: schemas.ExchangeCreate,
# ) -> Any:
#     """
#     Create new exchange.
#     """
#     exchange = crud.exchange.get_by_name(db, name=exchange_in.name)
#     if exchange:
#         raise HTTPException(
#             status_code=400,
#             detail="The exchange with this name already exists in the system.",
#         )
#
#     exchange = crud.exchange.create(db, obj_in=exchange_in)
#
#     return exchange


@router.get("/", response_model=List[schemas.Exchange], status_code=status.HTTP_200_OK)
def get_exchanges(db: Session = Depends(deps.get_db)):
    exchanges = crud.exchange.get_multi(db)
    return exchanges


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_exchange(*, db: Session = Depends(deps.get_db), id: int):
    return crud.exchange.get(db, id=id)
