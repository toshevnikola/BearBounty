from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.exchange import Exchange
from app.schemas.exchange import ExchangeCreate, ExchangeUpdate


class CRUDExchange(CRUDBase[Exchange, ExchangeCreate, ExchangeUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[Exchange]:
        return db.query(Exchange).filter(Exchange.name == name).first()


exchange = CRUDExchange(Exchange)
