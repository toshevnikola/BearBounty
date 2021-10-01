import datetime
import os

import psycopg2
from dataclasses import dataclass
from celery import Celery
from binance import Client

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
print(REDIS_PASSWORD)
print(REDIS_HOST)
CONN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

app = Celery('task',
             backend=f'redis://{REDIS_HOST}',
             broker=f'redis://{REDIS_HOST}',
             include=['tasks'])


@dataclass
class OrderMessage():
    trading_pair: str
    exchange: str
    timestamp: float
    signal: str
    user_exchange_id: int
    user_id: int
    bot_id: int
    base_order_amount: float


@dataclass
class BinanceClientWrapper:
    def __init__(self, order_message: OrderMessage):
        self.order_message = order_message
        self.api_key, self.secret_key = self.get_user_exchange_keys()
        self.client = Client(self.api_key, self.secret_key, testnet=True)
        self.client.API_URL = 'https://testnet.binance.vision/api'

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
        new_deal_query = f"""insert into deal(bot_id, pair, is_active, created_at, updated_at)
                values({self.order_message.bot_id},'{self.order_message.trading_pair}', true, '{now}', '{now}') returning id as deal_id"""
        self.client.create_test_order(
            symbol=self.order_message.trading_pair,
            side='BUY',
            type='MARKET',
            quoteOrderQty=self.order_message.base_order_amount)
        with conn.cursor() as curs:
            curs.execute(new_deal_query)
            deal_id = curs.fetchone()[0]
            now = datetime.datetime.utcnow()
            new_order_query = f"""insert into "order"(deal_id, amount, fee, status, created_at, updated_at) 
                              values({deal_id}, {self.order_message.base_order_amount}, 0, 'active', '{now}', '{now}')"""
            curs.execute(new_order_query)
        conn.commit()
        conn.close()


@app.task
def start_deal(data: dict):
    order_message = OrderMessage(**data)
    client = BinanceClientWrapper(order_message)
    client.start_deal()
    return data
