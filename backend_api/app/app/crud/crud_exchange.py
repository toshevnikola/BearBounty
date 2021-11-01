from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.exchange import Exchange
from app.schemas.exchange import ExchangeCreate, ExchangeUpdate


class CRUDExchange(CRUDBase[Exchange, ExchangeCreate, ExchangeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Exchange]:
        return db.query(Exchange).filter(Exchange.name == name).first()

    def get_client_balance(
        self, db: Session, *, exchange_id: int, api_key: str, api_secret: str
    ) -> Optional[list]:
        exchange_: Exchange = db.query(Exchange).get(exchange_id)
        print(exchange_.name)
        return exchange_.get_client_balance(api_key=api_key, secret_key=api_secret)


exchange = CRUDExchange(Exchange)
