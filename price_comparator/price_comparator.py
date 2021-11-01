import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
import psycopg2
import psycopg2.extras
import redis
from binance import Client

all_deals = """
              select d.*,
              d2.take_profit_pct, d2.safety_order_amount, d2.safety_order_price_deviation_pct, d2.max_safety_orders,
              u.api_key, u.api_secret, e.name as exchange_name
              from deal d join dcabot d2 on d2.id = d.bot_id 
              join userexchange u on d2.user_exchange_id = u.id 
              join exchange e on e.id = u.exchange_id
              where d.is_active=True
            """
orders_for_deal_query = """select d.id, d.bot_id, d.pair as trading_pair, o.*
                           from "order" o join deal d on o.deal_id = d.id 
                           where d.id={}
                        """
QUERIES = {"all_active_deals": all_deals}

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
CONN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

redis_conn = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
pubsub = redis_conn.pubsub()


def publish(channel: str, message: dict):
    print(f'Publishing event with message:{message}')
    redis_conn.publish(channel=channel, message=json.dumps(message))


@dataclass()
class Order:
    id: int
    deal_id: int
    amount: float
    fee: float
    status: str
    type: str
    created_at: datetime
    updated_at: datetime
    price: float
    exchange_order_id: int
    trading_pair: str

    def amount_x_price(self):
        return self.amount * self.price

    def is_active(self):
        return self.status == "active"

    def is_buy(self):
        return self.type == "buy"

    def is_sell(self):
        return self.type == 'sell'

    def is_completed(self):
        return self.status == "completed"

    def __gt__(self, other):
        return self.created_at > other.created_at

    def update_status(self, client: Client, conn) -> Optional[str]:
        current_exchange_status = client.get_order(symbol=self.trading_pair, orderId=self.exchange_order_id)
        if self.status == 'active':
            if current_exchange_status['status'] == 'FILLED':
                print(f'Changing status from active to completed for order {self.id}')
                self.change_status_in_db('completed', conn)
                if self.type == 'sell':
                    return 'DEAL DONE'
            elif current_exchange_status['status'] == 'CANCELED':
                print(f'Changing status from active to canceled for order {self.id}')
                self.change_status_in_db('canceled', conn)

    def change_status_in_db(self, status: str, conn):
        query = """update "order" set status = %s where id = %s"""
        cur = conn.cursor()
        cur.execute(query, (status, self.id))
        self.status = status
        conn.commit()
        cur.close()

    def cancel_order(self, client: Client, conn):
        resp = client.cancel_order(symbol=self.trading_pair, orderId=self.exchange_order_id)
        if resp['status'] == 'CANCELED':
            self.change_status_in_db('canceled', conn)


@dataclass
class Deal:
    id: int
    bot_id: int
    pair: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    orders: List[Optional[Order]]
    average_price: float
    take_profit_pct: float
    safety_order_amount: float
    safety_order_price_deviation_pct: float
    ticker: float
    exchange_name: str
    max_safety_orders: int

    def __init__(
            self,
            id: int,
            bot_id: int,
            pair: str,
            is_active: bool,
            created_at: datetime,
            updated_at: datetime,
            take_profit_pct: float,
            safety_order_amount: float,
            safety_order_price_deviation_pct: float,
            api_key: str,
            api_secret: str,
            exchange_name: str,
            max_safety_orders: int
    ):
        self.id = id
        self.bot_id = bot_id
        self.pair = pair
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
        self.orders = self.set_orders()
        self.take_profit_pct = take_profit_pct
        self.safety_order_amount = safety_order_amount
        self.safety_order_price_deviation_pct = safety_order_price_deviation_pct
        self.exchange_name = exchange_name
        self.max_safety_orders = max_safety_orders
        self.client = self.set_client(api_key=api_key, api_secret=api_secret, exchange_name=exchange_name)

    @staticmethod
    def set_client(api_key: str, api_secret: str, exchange_name: str) -> Client:
        return Client(api_key, api_secret, testnet=True) \
            if exchange_name in ('Test', 'Binance (testnet)') else Client(
            api_key, api_secret)

    def set_orders(self):
        conn = psycopg2.connect(CONN)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(orders_for_deal_query.format(self.id))
        orders = cursor.fetchall()
        dto_orders = []
        for order in orders:
            o = Order(
                id=order["id"],
                deal_id=order["deal_id"],
                amount=order["amount"],
                fee=order["fee"],
                status=order["status"],
                type=order["type"],
                created_at=order["created_at"],
                updated_at=order["updated_at"],
                price=order["price"],
                exchange_order_id=order['exchange_order_id'],
                trading_pair=order['trading_pair']
            )
            dto_orders.append(o)
        return dto_orders

    def cancel_active_orders(self, order_type: str, conn):
        orders_to_cancel = [o for o in self.orders if o.type == order_type and o.status == 'active']
        for o in orders_to_cancel:
            print(f"Canceling order {o.id}")
            o.cancel_order(self.client, conn)

    def get_latest_and_next_price_to_buy(self) -> Tuple[float, float]:
        latest_order = max(
            o for o in self.orders if o.type == "buy" and o.status == "completed"
        )
        latest_price = latest_order.price
        next_price = (
                latest_price - latest_price * self.safety_order_price_deviation_pct / 100
        )
        return latest_price, next_price

    def set_average_price(self) -> None:
        total_amount = 0
        total_price = 0
        for o in self.orders:
            if o.is_buy() and o.is_completed():
                total_amount += o.amount
                total_price += o.amount_x_price()
        self.average_price = total_price / total_amount

    def get_pct_difference(self):
        ticker = next(
            (v["price"] for v in self.client.get_all_tickers() if v["symbol"] == self.pair)
        )
        ticker_float = float(ticker)
        self.ticker = ticker_float
        change_percent = (
                                 (float(ticker_float) - self.average_price) / self.average_price
                         ) * 100
        return change_percent

    @property
    def total_buy_orders(self):
        return self.max_safety_orders + 1

    def has_remaining_safety_orders(self) -> bool:
        completed_buy_orders = self.get_orders_with_type_and_status(type='buy', status='completed')
        if len(completed_buy_orders) >= self.total_buy_orders:
            print('All buy orders completed')
            return False
        return True

    def get_orders_with_type_and_status(self, type: str, status: str) -> List[Order]:
        return [o for o in self.orders if o.type == type and o.status == status]

    def take_action(self, conn):
        pct_difference = self.get_pct_difference()
        #
        # print(f"Pct diff for deal {self.id} = {pct_difference}%")
        # print(f"Target profit for deal {self.id} = {self.take_profit_pct}%")
        # print('------')
        if pct_difference > 0:
            print(pct_difference)
            # cancel previously created active buy orders
            self.cancel_active_orders('buy', conn)
            is_closer_to_target = (
                    abs(self.take_profit_pct - pct_difference) < pct_difference
            )
            if is_closer_to_target:
                order_msg = OrderMessage(
                    trading_pair=self.pair,
                    timestamp=time.time(),
                    deal_id=self.id,
                    amount=self.get_sell_amount(),
                    type="sell",
                    price=self.get_sell_price(),
                    exchange=self.exchange_name
                )
                if not self.has_active_sell_order():
                    publish("buy_order", vars(order_msg))
        elif pct_difference < 0:
            print(pct_difference)
            # delete previously created sell orders
            self.cancel_active_orders('sell', conn)
            if not self.has_active_buy_order() and self.has_remaining_safety_orders():
                latest_price, next_price = self.get_latest_and_next_price_to_buy()
                is_closer_to_next_buy_order = abs(next_price - self.ticker) < abs(
                    latest_price - self.ticker
                )
                if is_closer_to_next_buy_order:
                    # BUY
                    order_msg = OrderMessage(
                        trading_pair=self.pair,
                        timestamp=time.time(),
                        deal_id=self.id,
                        amount=self.get_buy_amount(),
                        type="buy",
                        price=next_price,
                        exchange=self.exchange_name
                    )
                    publish("buy_order", vars(order_msg))

    def get_buy_amount(self):
        return self.safety_order_amount * pow(
            self.safety_order_price_deviation_pct, len(self.orders) - 1
        )

    def get_sell_amount(self) -> float:
        return sum([o.amount for o in self.orders if o.is_buy() and o.is_completed()])

    def update_order_statuses(self, conn) -> bool:
        close_deal = False
        for o in self.orders:
            res = o.update_status(self.client, conn=conn)
            if res == 'DEAL DONE':
                print(f"Deal{self.id}: DONE")
                close_deal = True
        return close_deal

    def get_sell_price(self):
        return self.average_price + self.average_price * self.take_profit_pct / 100

    def close(self, conn):
        print('Closing deal...')
        cursor = conn.cursor()
        """this method is used to close the deal"""
        inactive_deal_query = """update "deal" set is_active = %s where id = %s;"""
        bot_not_in_deal_query = """update "dcabot" set in_deal = %s where id = %s """
        cursor.execute(inactive_deal_query, (False, self.id))
        cursor.execute(bot_not_in_deal_query, (False, self.bot_id))
        conn.commit()
        cursor.close()
        print(f'Deal with id {self.id} closed.')
        print(f'DCABot {self.bot_id} is not in deal.')

    def has_active_sell_order(self):
        for o in self.orders:
            if o.is_sell() and o.is_active():
                return True
        return False

    def has_active_buy_order(self) -> bool:
        for o in self.orders:
            if o.is_buy() and o.is_active():
                return True
        return False


@dataclass
class OrderMessage:
    trading_pair: str
    timestamp: float
    deal_id: int
    amount: float
    type: str
    price: float
    exchange: str


def get_all_active_deals(conn):
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    curs.execute(QUERIES["all_active_deals"])
    results = curs.fetchall()
    return results


def main():
    conn = psycopg2.connect(CONN)
    deals = get_all_active_deals(conn)
    for deal in deals:
        d = Deal(
            id=deal["id"],
            bot_id=deal["bot_id"],
            pair=deal["pair"],
            is_active=deal["is_active"],
            created_at=deal["created_at"],
            updated_at=deal["updated_at"],
            take_profit_pct=deal["take_profit_pct"],
            safety_order_amount=deal["safety_order_amount"],
            safety_order_price_deviation_pct=deal["safety_order_price_deviation_pct"],
            api_key=deal['api_key'],
            api_secret=deal['api_secret'],
            exchange_name=deal['exchange_name'],
            max_safety_orders=deal['max_safety_orders']
        )
        print(f'For deal {d.id}')

        should_close_deal = d.update_order_statuses(conn)
        if should_close_deal:
            print('Should close deal...')
            d.close(conn)
        else:
            d.set_average_price()
            d.take_action(conn)
        print('-------------------')


if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)
