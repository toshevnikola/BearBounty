import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ARRAY,
    Float,
    ForeignKey,
)
from app.db.base_class import Base

from app.models.user_exchange import UserExchange  # noqa


class DCABot(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    required_balance = Column(Float, default=True)
    base_coin = Column(String, nullable=False)
    base_order_amount = Column(Float, nullable=False)
    safety_order_amount = Column(Float, nullable=False)
    max_safety_orders = Column(Integer, nullable=False)
    max_active_safety_orders = Column(Integer, nullable=False)
    safety_order_price_deviation_pct = Column(Float, nullable=False)
    safety_order_price_deviation_scale = Column(Float, nullable=False)
    allocated_funds = Column(Float)
    trading_pairs = Column(ARRAY(String))
    consider_overall_sentiment = Column(Boolean, default=False)
    stop_loss_pct = Column(Float, nullable=True)
    take_profit_pct = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    is_running = Column(Boolean, default=True)
    in_deal = Column(Boolean, default=False)
    user_exchange_id = Column(Integer, ForeignKey(UserExchange.id), index=True)
