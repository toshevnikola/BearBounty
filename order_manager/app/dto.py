import datetime
import math
from dataclasses import dataclass

import psycopg2
from binance import Client

from order_manager.app.settings import CONN


@dataclass
class StartDealOrderMessage:
    trading_pair: str
    exchange: str
    timestamp: float
    signal: str
    user_exchange_id: int
    user_id: int
    bot_id: int
    base_order_amount: float


@dataclass
class OrderMessage:
    trading_pair: str
    timestamp: float
    deal_id: int
    amount: float
    type: str
    price: float
    exchange: str


@dataclass
class BinanceClientWrapper:
    api_key: str
    secret_key: str
    client: Client

    def __init__(self, order_message: OrderMessage):
        self.order_message = order_message

    def set_user_exchange_keys(self):
        conn = psycopg2.connect(CONN)
        query = f"""select api_key, api_secret from userexchange join dcabot d on userexchange.id = d.user_exchange_id join deal d2 on d.id = d2.bot_id where d2.id={self.order_message.deal_id}"""
        with conn.cursor() as curs:
            curs.execute(query)
            result = curs.fetchone()
        conn.close()
        self.api_key, self.secret_key = result[0], result[1]
        self.client = self.set_client(
            self.api_key, self.secret_key, self.order_message.exchange
        )

    @staticmethod
    def set_client(api_key: str, api_secret: str, exchange_name: str) -> Client:
        return (
            Client(api_key, api_secret, testnet=True)
            if exchange_name in ("Test", "Binance (testnet)")
            else Client(api_key, api_secret)
        )

    def round_down(self, pair, number):
        info = self.client.get_symbol_info(pair)
        step_size = [
            float(_["stepSize"])
            for _ in info["filters"]
            if _["filterType"] == "LOT_SIZE"
        ][0]
        step_size = f"{step_size}.8f"
        step_size = step_size.rstrip("0")
        decimals = len(step_size.split(".")[1])
        return math.floor(number * 10 ** decimals) / 10 ** decimals

    @staticmethod
    def round_number_to_step_size(
        info: dict, number: float, filter_: str, filter_tick_param: str
    ) -> float:
        step_size = [
            float(_[filter_tick_param])
            for _ in info["filters"]
            if _["filterType"] == filter_
        ][0]
        fraction = step_size
        decimal_places = abs(int(f"{fraction:e}".split("e")[-1]))
        print(decimal_places)
        return round(number, decimal_places)

    def add_order(self):
        conn = psycopg2.connect(CONN)
        now = datetime.datetime.utcnow()
        # check bot in deal
        with conn.cursor() as curs:
            curs.execute(
                f"""select * from deal join "order" o on deal.id = o.deal_id where deal.id = {self.order_message.deal_id} and o.status='active' """
            )
            active_orders = curs.fetchall()
            if len(active_orders) > 0:
                print("Skipping. Active order already exists!")
                return

            info = self.client.get_symbol_info(self.order_message.trading_pair)
            quantity = self.round_number_to_step_size(
                info=info,
                number=self.order_message.amount / self.order_message.price,
                filter_="LOT_SIZE",
                filter_tick_param="stepSize",
            )
            price = self.round_number_to_step_size(
                info=info,
                number=self.order_message.price,
                filter_="PRICE_FILTER",
                filter_tick_param="tickSize",
            )
            order_rsp = self.client.create_order(
                symbol=self.order_message.trading_pair,
                side=str(self.order_message.type).upper(),
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC",
            )
            print(order_rsp)
            order_id = order_rsp["orderId"]
            new_order_query = f"""
                               LOCK TABLE "order" IN ACCESS EXCLUSIVE MODE;
                                 insert into "order"(deal_id, amount, fee, type, status, created_at, updated_at, price, exchange_order_id) 
                                 values({self.order_message.deal_id}, {self.order_message.amount}, 0, '{self.order_message.type}', 'active', '{now}', '{now}', {price}, {order_id});
                               """
            curs.execute(new_order_query)
            conn.commit()
        conn.close()
        return order_rsp


@dataclass
class BinanceClientWrapperStartDeal:
    def __init__(self, order_message: StartDealOrderMessage):
        self.order_message = order_message
        self.api_key, self.secret_key = self.get_user_exchange_keys()
        self.client = self.set_client(
            self.api_key, self.secret_key, order_message.exchange
        )

    @staticmethod
    def set_client(api_key: str, api_secret: str, exchange_name: str) -> Client:
        return (
            Client(api_key, api_secret, testnet=True)
            if exchange_name in ("Test", "Binance (testnet)")
            else Client(api_key, api_secret)
        )

    def get_user_exchange_keys(self) -> [str, str]:
        conn = psycopg2.connect(CONN)
        query = f"""select api_key, api_secret from userexchange where id={self.order_message.user_exchange_id}"""
        with conn.cursor() as curs:
            curs.execute(query)
            result = curs.fetchone()
        conn.close()
        return result[0], result[1]

    def start_deal(self):
        conn = psycopg2.connect(CONN)
        now = datetime.datetime.utcnow()
        # check bot in deal
        with conn.cursor() as curs:
            curs.execute(
                f"select in_deal from dcabot where dcabot.id = {self.order_message.bot_id}"
            )
            bot_in_deal = curs.fetchone()[0]
        if bot_in_deal:
            print("SKIPPING! Bot is already in deal!")
            return
        new_deal_query = f"""insert into deal(bot_id, pair, is_active, created_at, updated_at)
                values({self.order_message.bot_id},'{self.order_message.trading_pair}', true, '{now}', '{now}') returning id as deal_id"""
        set_bot_in_deal_query = f"update dcabot set in_deal=true where dcabot.id={self.order_message.bot_id};"
        with conn.cursor() as curs:
            curs.execute(set_bot_in_deal_query)
            curs.execute(new_deal_query)
            deal_id = curs.fetchone()[0]
            now = datetime.datetime.utcnow()
            order_rsp = self.client.create_order(
                symbol=self.order_message.trading_pair,
                side="BUY",
                type="MARKET",
                quoteOrderQty=self.order_message.base_order_amount,
            )
            order_id = order_rsp["orderId"]
            fills = order_rsp.get("fills", None)
            if fills:
                price = fills[0].get("price", None)
                if price:
                    price = float(price)
                    new_order_query = f"""insert into "order"(deal_id, amount, fee, type, status, created_at, updated_at, price, exchange_order_id) 
                                                  values({deal_id}, {self.order_message.base_order_amount}, 0,'buy', 'completed', '{now}', '{now}', {price},{order_id})"""
                    curs.execute(new_order_query)

        conn.commit()
        conn.close()
