import datetime
from typing import TYPE_CHECKING, Union, Optional
from binance import Client, exceptions
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Exchange(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    supported_pairs = Column(ARRAY(String))
    is_available = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    user_exchange = relationship("UserExchange", back_populates="exchange")

    def get_client_balance(self, api_key: str, secret_key: str) -> Optional[list]:
        if self.name == "Test" or self.name == "Binance (testnet)":
            client = Client(api_key, secret_key, testnet=True)
        elif self.name == "Binance":
            print("Binance client")
            client = Client(api_key, secret_key)
        else:
            client = None
        try:
            info = client.get_account()
            # print("Info:",info)
            tickers = [
                t for t in client.get_all_tickers() if str(t["symbol"]).endswith("USDT")
            ]
            # print("tickers", tickers)
            items_to_check = [
                item for item in info["balances"] if float(item["free"]) > 0
            ]
            print("items to check:", items_to_check)
            return self.__all_assets(items_to_check=items_to_check, tickers=tickers)
        except exceptions.BinanceAPIException as e:
            print(e)
            return None

    @staticmethod
    def __all_assets(items_to_check: list, tickers: list) -> list:
        with_tickers = []
        for t in tickers:
            print(t)
            asset_only = t["symbol"].replace("USDT", "")
            for item in items_to_check:
                if asset_only in item["asset"]:
                    with_tickers.append(dict(**item, **t))
        print("before usdt_")
        USDT_ = [i for i in items_to_check if i["asset"] == "USDT"][0]
        with_tickers.append(USDT_)
        print("-------------------------")
        print(with_tickers)
        print("-------------------------")
        return with_tickers
