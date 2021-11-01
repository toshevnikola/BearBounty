from celery import Celery
from order_manager.app.dto import (
    StartDealOrderMessage,
    BinanceClientWrapperStartDeal,
    OrderMessage,
    BinanceClientWrapper,
)
from order_manager.app.settings import REDIS_HOST

app = Celery(
    "task",
    backend=f"redis://{REDIS_HOST}",
    broker=f"redis://{REDIS_HOST}",
    include=["tasks"],
)


@app.task
def start_deal(data: dict):
    order_message = StartDealOrderMessage(**data)
    client = BinanceClientWrapperStartDeal(order_message=order_message)
    client.start_deal()
    return data


@app.task
def new_order(data: dict):
    order_message = OrderMessage(**data)
    client = BinanceClientWrapper(order_message=order_message)
    client.set_user_exchange_keys()
    client.add_order()
