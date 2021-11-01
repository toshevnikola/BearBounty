from typing import Any, Dict, Optional, Union, List

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_exchange import UserExchange
from app.models.exchange import Exchange
from app.schemas.user_exchange import UserExchangeCreate, UserExchangeUpdate
import crud


class CRUDUserExchange(CRUDBase[UserExchange, UserExchangeCreate, UserExchangeUpdate]):
    def get_by_user_and_exchange(
        self, db: Session, user_id: int, exchange_id: int
    ) -> Optional[UserExchange]:
        return (
            db.query(UserExchange)
            .filter(
                UserExchange.user_id == user_id, UserExchange.exchange_id == exchange_id
            )
            .first()
        )

    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: UserExchangeCreate,
        user_id: int,
    ) -> UserExchange:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)  # type: ignore
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail=f"Exchange with id {obj_in.exchange_id} does not exist",
            )

    def get_by_user(self, db: Session, user_id: int) -> List[UserExchange]:
        return (
            db.query(UserExchange)
            .join(UserExchange.exchange)
            .filter(UserExchange.user_id == user_id)
            .all()
        )

    def get_with_refreshed_assets(self, db: Session, id: int) -> Optional[UserExchange]:
        ue: UserExchange = db.query(UserExchange).filter(UserExchange.id == id).first()
        if ue:
            refreshed_assets = ue.get_refreshed_assets()
            setattr(ue, "assets", refreshed_assets)
            db.add(ue)
            db.commit()
            db.refresh(ue)
            return ue

    def check_valid(self, db: Session, id: int) -> bool:
        pass


user_exchange = CRUDUserExchange(UserExchange)
