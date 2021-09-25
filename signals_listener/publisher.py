import asyncio
import json
import os
import time
import asyncpg
import redis
from tradingview_ta import TA_Handler
from typing import Set
from dataclasses import dataclass

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
CONN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
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
class BuyOrderSignal:
    trading_pair: str
    exchange: str
    timestamp: float
    signal: str


async def get_pairs_to_check() -> Set[PairToCheck]:
    conn = await asyncpg.connect(CONN)
    query = """select dcabot.trading_pairs, e.name as exchange_name from dcabot
         join userexchange u on dcabot.user_exchange_id = u.id
         join exchange e on e.id = u.exchange_id
         where dcabot.is_running=True;"""
    results = await conn.fetch(query)
    pairs_to_check = set()
    for r in results:
        for tp in r["trading_pairs"]:
            p = PairToCheck(trading_pair=tp, exchange=r["exchange_name"])
            pairs_to_check.add(p)

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
        for r in results:
            summary = await check_signal(symbol=r.trading_pair, interval="15m")
            print(summary)
            if summary in ["BUY", "STRONG_BUY"]:
                buy_order_signal = BuyOrderSignal(
                    trading_pair=r.trading_pair,
                    exchange=r.exchange,
                    timestamp=time.time(),
                    signal=summary,
                )
                publish("buy_order", vars(buy_order_signal))

        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
