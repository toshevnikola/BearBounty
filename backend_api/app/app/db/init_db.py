from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401


def init_db(db: Session) -> None:
    exchange = crud.exchange.get_by_name(db, name="Binance")
    if not exchange:
        exchange_in = schemas.ExchangeCreate(
            name="Binance",
            pairs=[
                "BTCUSDT",
                "ETHUSDT",
                "BNBUSDT",
                "SOLUSDT",
                "DYDXUSDT",
                "AVAXUSDT",
                "XRPUSDT",
                "DOTUSDT",
                "ADAUSDT",
                "COTIUSDT",
                "LUNAUSDT",
                "FILUSDT",
                "FTMUSDT",
                "OMGUSDT",
                "ATOMUSDT",
            ],
        )
        exchange = crud.exchange.create(db, obj_in=exchange_in)  # noqa: F841
