import datetime

from binance import Client, exceptions
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ARRAY,
    Float,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.exchange import Exchange  # noqa
from app.models.user import User  # noqa


class UserExchange(Base):
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String)
    api_secret = Column(String)
    balance = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    exchange_id = Column(Integer, ForeignKey(Exchange.id), index=True)
    exchange = relationship("Exchange", back_populates="user_exchange")
    is_valid = Column(Boolean)
    assets = Column(ARRAY(JSON))

    def get_refreshed_assets(self):
        if self.exchange.name == "Test" or self.exchange.name == "Binance (testnet)":
            client = Client(self.api_key, self.api_secret, testnet=True)
        elif self.exchange.name == "Binance":
            client = Client(self.api_key, self.api_secret)
        else:
            client = None
        try:
            info = client.get_account()
            tickers = [
                t for t in client.get_all_tickers() if str(t["symbol"]).endswith("USDT")
            ]
            items_to_check = [
                item
                for item in info["balances"]
                if float(item["free"]) > 0 or float(item["locked"])
            ]
            return self.__all_assets(items_to_check=items_to_check, tickers=tickers)
        except exceptions.BinanceAPIException as e:
            print(e)
            return None

    @staticmethod
    def __all_assets(items_to_check: list, tickers: list) -> list:
        with_tickers = []
        for t in tickers:
            asset_only = t["symbol"].replace("USDT", "")
            for item in items_to_check:
                if asset_only in item["asset"]:
                    with_tickers.append(dict(**item, **t))
        with_tickers = []
        for t in tickers:
            asset_only = t["symbol"].replace("USDT", "")
            for item in items_to_check:
                if asset_only in item["asset"]:
                    with_tickers.append(dict(**item, **t))

        USDT_ = [i for i in items_to_check if i["asset"] == "USDT"]
        if USDT_:
            with_tickers.append(USDT_[0])

        return with_tickers
