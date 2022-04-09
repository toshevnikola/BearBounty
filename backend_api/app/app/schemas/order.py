from datetime import datetime

from pydantic import BaseModel

from constants import OrderStatusEnum, OrderTypeEnum


class Order(BaseModel):
    id: int
    deal_id: int
    amount: float
    fee: float
    status: OrderStatusEnum
    type: OrderTypeEnum
    exchange_order_id: int
    created_at: datetime
    updated_at: datetime
    price: float
