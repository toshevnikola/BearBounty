from typing import List

from sqlalchemy.orm import Session

from app.models import Deal
from app.schemas import DealCreate, DealUpdate
from app.crud.base import CRUDBase
from app.models import DCABot, UserExchange, User


class CRUDDeal(CRUDBase[Deal, DealCreate, DealUpdate]):
    def get_by_user(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 10
    ) -> List[Deal]:
        return (
            db.query(Deal)
            .join(DCABot)
            .join(UserExchange)
            .join(User)
            .filter(
                Deal.bot_id == DCABot.id,
                DCABot.user_exchange_id == UserExchange.id,
                UserExchange.user_id == user_id,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user_exchange(
        self, db: Session, user_exchange_id: int, skip: int = 0, limit: int = 10
    ) -> List[Deal]:
        return (
            db.query(Deal)
            .join(DCABot)
            .join(UserExchange)
            .filter(
                Deal.bot_id == DCABot.id,
                DCABot.user_exchange_id == UserExchange.id,
                UserExchange.id == user_exchange_id,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


deal = CRUDDeal(Deal)
