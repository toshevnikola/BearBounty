from celery import Celery
from order_manager.app.dto import OrderMessage, BinanceClientWrapper
from order_manager.app.settings import REDIS_HOST

app = Celery('task',
             backend=f'redis://{REDIS_HOST}',
             broker=f'redis://{REDIS_HOST}',
             include=['tasks'])


@app.task
def start_deal(data: dict):
    order_message = OrderMessage(**data)
    client = BinanceClientWrapper(order_message)
    client.start_deal()
    return data
