import json
import os

from order_manager.tasks import start_deal

import redis

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
redis_conn = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
pubsub = redis_conn.pubsub()


def main():
    print('Started subscriber to buy_order...')
    pubsub.subscribe('buy_order')
    for message in pubsub.listen():
        print(f'Received message:{message}')
        if message.get('type') == 'message':
            data = json.loads(message.get("data"))
            start_deal.delay(data)


if __name__ == '__main__':
    main()
