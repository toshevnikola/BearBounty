import asyncio
import json
import os
import time
from collections import defaultdict

import asyncpg
import redis
from tradingview_ta import TA_Handler
from typing import Set, Dict, List
from dataclasses import dataclass

from sql_queries import pairs_to_check_query

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
CONN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_PASSWORD = None
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

redis_conn = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
pubsub = redis_conn.pubsub()


def publish(channel: str, message: dict):
    redis_conn.publish(channel=channel, message=json.dumps(message))


@dataclass(eq=True, unsafe_hash=True)
class PairToCheck:
    trading_pair: str
    exchange: str


@dataclass()
class PotentialOrder:
    trading_pair: str
    exchange: str
    user_exchange_id: int
    user_id: int
    bot_id: int
    base_order_amount: float


@dataclass()
class BuyOrderSignal:
    trading_pair: str
    exchange: str
    timestamp: float
    signal: str
    user_exchange_id: int
    user_id: int
    bot_id: int
    base_order_amount: float


async def get_pairs_to_check() -> Dict[PairToCheck, List[PotentialOrder]]:
    conn = await asyncpg.connect(CONN)
    results = await conn.fetch(pairs_to_check_query)
    pairs_to_check = defaultdict(list)
    for r in results:
        for tp in r["trading_pairs"]:
            pair = PairToCheck(trading_pair=tp, exchange=r["exchange_name"])
            potential_order = PotentialOrder(trading_pair=tp, exchange=r['exchange_name'],
                                             user_exchange_id=r['user_exchange_id'],
                                             bot_id=r['bot_id'],
                                             user_id=r['user_id'],
                                             base_order_amount=r['base_order_amount'])

            pairs_to_check[pair].append(potential_order)

    await conn.close()
    return pairs_to_check


async def check_signal(
        symbol: str, interval: str, screener: str = "crypto", exchange: str = "BINANCE"
) -> str:
    tv = TA_Handler(
        symbol=symbol, screener=screener, exchange=exchange, interval=interval
    )
    analyse = tv.get_analysis()
    return analyse.summary["RECOMMENDATION"]


async def main():
    while True:
        results = await get_pairs_to_check()
        for pair_to_check, potential_orders in results.items():
            summary = await check_signal(symbol=pair_to_check.trading_pair, interval="15m")
            print(summary)
            if summary in ["BUY", "STRONG_BUY"]:
                for potential_order in potential_orders:
                    buy_order_signal = BuyOrderSignal(
                        trading_pair=pair_to_check.trading_pair,
                        exchange=pair_to_check.exchange,
                        timestamp=time.time(),
                        signal=summary,
                        user_exchange_id=potential_order.user_exchange_id,
                        user_id=potential_order.user_id,
                        bot_id=potential_order.bot_id,
                        base_order_amount=potential_order.base_order_amount
                    )
                    print(buy_order_signal)
                    publish("buy_order", vars(buy_order_signal))

        await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
