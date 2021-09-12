from typing import Any, Dict, Optional, Union, List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.dca_bot import DCABot
from app.schemas.dca_bot import DCABotCreate, DCABotUpdate
from app.models import UserExchange


class CRUDDCABot(CRUDBase[DCABot, DCABotCreate, DCABotUpdate]):
    def get_by_user_exchange(self, db: Session, user_exchange_id: int) -> List[DCABot]:
        return (
            db.query(DCABot).filter(DCABot.user_exchange_id == user_exchange_id).all()
        )

    def get_by_user(self, db: Session, user_id: int) -> List[DCABot]:
        return (
            db.query(DCABot)
            .join(UserExchange)
            .filter(UserExchange.user_id == user_id)
            .all()
        )

    def create(self, db: Session, *, obj_in: DCABotCreate) -> DCABot:
        obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data, required_balance=1000)  # type: ignore
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail=f"User Exchange with id {obj_in.user_exchange_id} does not exist",
            )

    def get_single(self, db: Session, id: int, user_id: int) -> Optional[DCABot]:
        return (
            db.query(DCABot)
            .join(UserExchange)
            .filter(DCABot.id == id, UserExchange.user_id == user_id)
            .first()
        )


dca_bot = CRUDDCABot(DCABot)
