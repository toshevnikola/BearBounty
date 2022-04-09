from __future__ import annotations
from typing import Optional, List, Any
from pydantic import BaseModel


# Shared properties


class DCABotBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_color: Optional[str] = None
    trading_pairs: List[str] = []
    base_coin: Optional[str] = None
    base_order_amount: Optional[float] = None
    safety_order_amount: Optional[float] = None
    max_safety_orders: Optional[int] = None
    max_active_safety_orders: Optional[int] = None
    safety_order_price_deviation_pct: Optional[float] = None
    safety_order_price_deviation_scale: Optional[float] = None
    allocated_funds: Optional[float] = None
    consider_overall_sentiment: Optional[bool] = None
    stop_loss_pct: Optional[float] = None
    take_profit_pct: Optional[float] = None
    is_running: Optional[bool]
    in_deal: Optional[bool]
    deals: Optional[List[Any]] = []


# Properties to receive via API on creation
class DCABotCreate(DCABotBase):
    name: str
    description: str
    avatar_color: str
    trading_pairs: List[str]
    base_coin: str
    base_order_amount: float
    safety_order_amount: float
    max_safety_orders: int
    max_active_safety_orders: int
    safety_order_price_deviation_pct: float
    safety_order_price_deviation_scale: float
    allocated_funds: float
    consider_overall_sentiment: bool = False
    stop_loss_pct: Optional[float] = None
    take_profit_pct: float
    user_exchange_id: int


# Properties to receive via API on update
class DCABotUpdate(DCABotBase):
    name: Optional[str]
    description: Optional[str]
    avatar_color: Optional[str]
    trading_pairs: Optional[List[str]]
    base_coin: Optional[str]
    base_order_amount: Optional[float]
    safety_order_amount: Optional[float]
    max_safety_orders: Optional[int]
    max_active_safety_orders: Optional[int]
    safety_order_price_deviation_pct: Optional[float]
    safety_order_price_deviation_scale: Optional[float]
    allocated_funds: Optional[float]
    consider_overall_sentiment: Optional[bool] = False
    stop_loss_pct: Optional[float] = None
    take_profit_pct: Optional[float]
    is_running: Optional[bool]


class DCABotInDBBase(DCABotBase):
    id: Optional[int] = None
    user_exchange_id: Optional[int] = None

    class Config:
        orm_mode = True


class DCABotInDB(DCABotInDBBase):
    pass


# Additional properties to return via API
class DCABot(DCABotInDBBase):
    pass
