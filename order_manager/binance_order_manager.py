import json
import os
from dataclasses import dataclass
from multiprocessing.context import Process

import asyncpg

from order_manager.tasks import make_binance_order
import psycopg2

import redis

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
redis_conn = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
pubsub = redis_conn.pubsub()
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')


def main():
    pubsub.subscribe('buy_order')
    for message in pubsub.listen():
        if message.get('type') == 'message':
            data = json.loads(message.get("data"))
            make_binance_order.delay(data)


if __name__ == '__main__':
    main()
