import os
from asyncio import sleep
from dataclasses import dataclass

import psycopg2
from celery import Celery

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
CONN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

app = Celery('task',
             backend='redis://localhost',
             broker='redis://localhost',
             include=['order_manager.tasks'])


@dataclass
class BinanceClient:
    def __init__(self, user_exchange_id: int):
        self.user_exchange_id = user_exchange_id
        self.api_key, self.secret_key = self.get_user_exchange_keys()

    def get_user_exchange_keys(self) -> [str, str]:
        conn = psycopg2.connect(CONN)
        query = f"""select api_key, api_secret from userexchange where id={self.user_exchange_id}"""
        with conn.cursor() as curs:
            curs.execute(query)
            result = curs.fetchone()
        return result[0], result[1]


@app.task
def make_binance_order(data: dict):
    client = BinanceClient(data['user_exchange_id'])
    print(client)
    return data
