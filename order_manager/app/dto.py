import datetime
from dataclasses import dataclass

import psycopg2
from binance import Client

from order_manager.app.settings import CONN


@dataclass
class OrderMessage:
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
        # check bot in deal
        with conn.cursor() as curs:
            curs.execute(f'select in_deal from dcabot where dcabot.id = {self.order_message.bot_id}');
            bot_in_deal = curs.fetchone()[0]
        if bot_in_deal:
            print('SKIPPING! Bot is already in deal!')
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
                side='BUY',
                type='MARKET',
                quoteOrderQty=self.order_message.base_order_amount)
            fills = order_rsp.get('fills', None)
            if fills:
                price = fills[0].get('price', None)
                if price:
                    price = float(price)
                    new_order_query = f"""insert into "order"(deal_id, amount, fee, status, created_at, updated_at, price) 
                                                  values({deal_id}, {self.order_message.base_order_amount}, 0, 'active', '{now}', '{now}', {price})"""
                    curs.execute(new_order_query)

        conn.commit()
        conn.close()
